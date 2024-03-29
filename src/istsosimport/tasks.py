import csv
from datetime import datetime
import math
import os
import logging


from locale import atof

from flask import render_template
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from sqlalchemy import exc, update, func


from istsosimport.utils.celery import celery_app
from istsosimport.utils.mail import send_mail
from istsosimport.env import FILE_ERROR_DIRECTORY, db
from istsosimport.db.models import EventTime, Import, Measure, Procedure
from istsosimport.db.utils import get_schema_session
from istsosimport.schemas import EvenTimeSchema


log = logging.getLogger()


@celery_app.task(bind=True)
def import_data(self, import_dict, filename, separator, config, csv_mapping, service):
    procedure_dict = import_dict["procedure"]
    file_eror_name = str(
        procedure_dict["name_prc"] + "_" + str(datetime.now()) + ".csv"
    )

    file_error = open(str(FILE_ERROR_DIRECTORY / file_eror_name), "w")
    with open(os.path.join(config["UPLOAD_FOLDER"], filename)) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator)
        columns_for_error_file = csvreader.fieldnames.copy()
        columns_for_error_file.append("error_reason")
        csv_writer = csv.DictWriter(
            file_error, delimiter=separator, fieldnames=columns_for_error_file
        )
        csv_writer.writeheader()
        total_succeed = 0
        total_rows = 0
        error_message = []
        val_col = None
        for row in csvreader:
            total_rows = total_rows + 1
            try:
                date_col = csv_mapping[
                    "urn:ogc:def:parameter:x-istsos:1.0:time:iso8601"
                ]
                event_time_dict = EvenTimeSchema().load(
                    {
                        "id_prc_fk": procedure_dict["id_prc"],
                        "time_eti": row[date_col],
                        "timezone": import_dict["timezone"],
                    },
                    unknown=EXCLUDE,
                )
                eventtime = EventTime(**event_time_dict)
                for proc in procedure_dict["proc_obs"]:
                    val_col = csv_mapping[proc["observed_property"]["def_opr"]]
                    floated_value = atof(row[val_col])
                    measure = Measure(val_msr=floated_value, id_pro_fk=proc["id_pro"])
                    measure.set_quality(proc)
                    eventtime.measures.append(measure)
                db.session.add(eventtime)
                db.session.commit()
                total_succeed = total_succeed + 1
            # validation Error : the date is not correct - ValueError : float cast error
            except ValueError as e:
                mess = f"Error : {str(e)} \n Responsible column : {val_col}"
                log.error(mess)
                row["error_reason"] = mess
                error_message.append(mess)
                csv_writer.writerow(row)
            except ValidationError as e:
                mess = f"Error : {str(e)} \n Responsible column : {date_col}"
                log.error(mess)
                row["error_reason"] = mess
                error_message.append(mess)
                csv_writer.writerow(row)
            except exc.SQLAlchemyError as e:
                log.error(e)
                error_message.append(e)
                row["error_reason"] = e
                csv_writer.writerow(row)
                db.session.rollback()

        file_error.close()

    db.session.execute(
        update(Import)
        .where(Import.id_import == import_dict["id_import"])
        .values(
            nb_row_total=total_rows,
            nb_row_inserted=total_succeed,
            error_file=file_eror_name,
        )
    )
    db.session.execute(
        update(Procedure)
        .where(Procedure.id_prc == procedure_dict["id_prc"])
        .values(
            stime_prc=db.session.query(func.min(EventTime.time_eti))
            .select_from(EventTime)
            .filter_by(id_prc_fk=procedure_dict["id_prc"])
            .scalar(),
            etime_prc=db.session.query(func.max(EventTime.time_eti))
            .select_from(EventTime)
            .filter_by(id_prc_fk=procedure_dict["id_prc"])
            .scalar(),
        )
    )

    db.session.commit()
    template = render_template(
        "mail_template.html",
        import_dict=import_dict,
        nb_row_total=total_rows,
        nb_row_inserted=total_succeed,
        error_message=error_message,
    )

    send_mail(import_dict["email"], "Import IstSOS", template)
