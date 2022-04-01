/* wrist_db

 */
drop table IF EXISTS analysis;
drop table IF EXISTS medical_practitioner;
drop table IF EXISTS x_ray;



create table medical_practitioner
   (user_id 	int	NOT NULL ,
    user_name		varchar(255)	NOT NULL,
    user_password     varchar(40)    NOT NULL ,
    user_contact     varchar(40)     NOT NULL,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
    );


create table analysis
   (analysis_id int NOT NULL ,
    image_id 	int 	 ,
    user_id 	int	,
    user_feedback    varchar(255) NOT NULL,
    PRIMARY KEY(analysis_id),
    FOREIGN KEY (image_id) REFERENCES x_ray (image_id),
    FOREIGN KEY (user_id) REFERENCES medical_practitioner (user_id)
    );



create table x_ray
   (image_id 	int NOT NULL,
    image_1		longblob NOT NULL,
    image_2     longblob  NOT NULL,
    patient_num     int NOT NULL ,
    user_id 	int	,
    PRIMARY KEY(image_id),
    FOREIGN KEY (user_id) REFERENCES medical_practitioner (user_id)
    );


