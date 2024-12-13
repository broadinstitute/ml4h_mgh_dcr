
------- VISIT_DETAIL -------------
--HINT DISTRIBUTE ON KEY (person_id)
CREATE TABLE OMOP.VISIT_DETAIL (
			visit_detail_id bigint NOT NULL,
			person_id integer NOT NULL,
			visit_detail_concept_id integer NOT NULL,
			visit_detail_start_date date NOT NULL,
			visit_detail_start_datetime datetime NULL,
			visit_detail_end_date date NOT NULL,
			visit_detail_end_datetime datetime NULL,
			visit_detail_type_concept_id integer NOT NULL,
			provider_id integer NULL,
			care_site_id integer NULL,
			visit_detail_source_value varchar(50) NULL,
			visit_detail_source_concept_id Integer NULL,
			admitted_from_concept_id Integer NULL,
			admitted_from_source_value varchar(50) NULL,
			discharged_to_source_value varchar(50) NULL,
			discharged_to_concept_id integer NULL,
			preceding_visit_detail_id bigint NULL,
			parent_visit_detail_id bigint NULL,
			visit_occurrence_id bigint NOT NULL );

--add primary key
ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT xpk_VISIT_DETAIL PRIMARY KEY NONCLUSTERED (visit_detail_id);
 

-- add constraints
ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_person_id FOREIGN KEY (person_id) REFERENCES OMOP.PERSON (PERSON_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_visit_detail_concept_id FOREIGN KEY (visit_detail_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_visit_detail_type_concept_id FOREIGN KEY (visit_detail_type_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_provider_id FOREIGN KEY (provider_id) REFERENCES OMOP.PROVIDER (PROVIDER_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_care_site_id FOREIGN KEY (care_site_id) REFERENCES OMOP.CARE_SITE (CARE_SITE_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_visit_detail_source_concept_id FOREIGN KEY (visit_detail_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_admitted_from_concept_id FOREIGN KEY (admitted_from_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_discharged_to_concept_id FOREIGN KEY (discharged_to_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_preceding_visit_detail_id FOREIGN KEY (preceding_visit_detail_id) REFERENCES OMOP.VISIT_DETAIL (VISIT_DETAIL_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_parent_visit_detail_id FOREIGN KEY (parent_visit_detail_id) REFERENCES OMOP.VISIT_DETAIL (VISIT_DETAIL_ID);

ALTER TABLE OMOP.VISIT_DETAIL ADD CONSTRAINT fpk_VISIT_DETAIL_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES OMOP.VISIT_OCCURRENCE (VISIT_OCCURRENCE_ID);


-- create indices
CREATE CLUSTERED INDEX idx_visit_det_person_id_1 ON OMOP.visit_detail (person_id ASC);
CREATE INDEX idx_visit_det_concept_id_1 ON OMOP.visit_detail (visit_detail_concept_id ASC);
CREATE INDEX idx_visit_det_occ_id ON OMOP.visit_detail (visit_occurrence_id ASC);


------ DEVICE_EXPOSURE ---------
--HINT DISTRIBUTE ON KEY (person_id)
CREATE TABLE OMOP.DEVICE_EXPOSURE (
			device_exposure_id integer NOT NULL,
			person_id integer NOT NULL,
			device_concept_id integer NOT NULL,
			device_exposure_start_date date NOT NULL,
			device_exposure_start_datetime datetime NULL,
			device_exposure_end_date date NULL,
			device_exposure_end_datetime datetime NULL,
			device_type_concept_id integer NOT NULL,
			unique_device_id varchar(255) NULL,
			production_id varchar(255) NULL,
			quantity integer NULL,
			provider_id integer NULL,
			visit_occurrence_id bigint NULL,
			visit_detail_id bigint NULL,
			device_source_value varchar(50) NULL,
			device_source_concept_id integer NULL,
			unit_concept_id integer NULL,
			unit_source_value varchar(50) NULL,
			unit_source_concept_id integer NULL );


--key constraint
ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT xpk_DEVICE_EXPOSURE PRIMARY KEY NONCLUSTERED (device_exposure_id);


ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_person_id FOREIGN KEY (person_id) REFERENCES OMOP.PERSON (PERSON_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_device_concept_id FOREIGN KEY (device_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_device_type_concept_id FOREIGN KEY (device_type_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_provider_id FOREIGN KEY (provider_id) REFERENCES OMOP.PROVIDER (PROVIDER_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES OMOP.VISIT_OCCURRENCE (VISIT_OCCURRENCE_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_visit_detail_id FOREIGN KEY (visit_detail_id) REFERENCES OMOP.VISIT_DETAIL (VISIT_DETAIL_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_device_source_concept_id FOREIGN KEY (device_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_unit_concept_id FOREIGN KEY (unit_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

ALTER TABLE OMOP.DEVICE_EXPOSURE ADD CONSTRAINT fpk_DEVICE_EXPOSURE_unit_source_concept_id FOREIGN KEY (unit_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

-- create indices
CREATE CLUSTERED INDEX idx_device_person_id_1 ON OMOP.device_exposure (person_id ASC);
CREATE INDEX idx_device_concept_id_1 ON OMOP.device_exposure (device_concept_id ASC);
CREATE INDEX idx_device_visit_id_1 ON OMOP.device_exposure (visit_occurrence_id ASC);



------- NOTE -----------
--HINT DISTRIBUTE ON KEY (person_id)
CREATE TABLE OMOP.NOTE (
			note_id integer NOT NULL,
			person_id integer NOT NULL,
			note_date date NOT NULL,
			note_datetime datetime NULL,
			note_type_concept_id integer NOT NULL,
			note_class_concept_id integer NOT NULL,
			note_title varchar(250) NULL,
			note_text varchar(MAX) NOT NULL,
			encoding_concept_id integer NOT NULL,
			language_concept_id integer NOT NULL,
			provider_id integer NULL,
			visit_occurrence_id bigint NULL,
			visit_detail_id bigint NULL,
			note_source_value varchar(50) NULL,
			note_event_id integer NULL,
			note_event_field_concept_id integer NULL );


--add primary key
ALTER TABLE OMOP.NOTE ADD CONSTRAINT xpk_note PRIMARY KEY NONCLUSTERED (note_id);

-- add constraints
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_person_id FOREIGN KEY (person_id) REFERENCES OMOP.PERSON (PERSON_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_note_type_concept_id FOREIGN KEY (note_type_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_note_class_concept_id FOREIGN KEY (note_class_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_encoding_concept_id FOREIGN KEY (encoding_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_language_concept_id FOREIGN KEY (language_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_provider_id FOREIGN KEY (provider_id) REFERENCES OMOP.PROVIDER (PROVIDER_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES OMOP.VISIT_OCCURRENCE (VISIT_OCCURRENCE_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_visit_detail_id FOREIGN KEY (visit_detail_id) REFERENCES OMOP.VISIT_DETAIL (VISIT_DETAIL_ID);
ALTER TABLE OMOP.NOTE ADD CONSTRAINT fpk_note_note_event_field_concept_id FOREIGN KEY (note_event_field_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

-- create indices
CREATE CLUSTERED INDEX idx_note_person_id_1 ON OMOP.note (person_id ASC);
CREATE INDEX idx_note_concept_id_1 ON OMOP.note (note_type_concept_id ASC);
CREATE INDEX idx_note_visit_id_1 ON OMOP.note (visit_occurrence_id ASC);


----------- LOCATION --------------
--HINT DISTRIBUTE ON RANDOM
CREATE TABLE OMOP.LOCATION (
			location_id integer NOT NULL,
			address_1 varchar(50) NULL,
			address_2 varchar(50) NULL,
			city varchar(50) NULL,
			state varchar(2) NULL,
			zip varchar(9) NULL,
			county varchar(20) NULL,
			location_source_value varchar(50) NULL,
			country_concept_id integer NULL,
			country_source_value varchar(80) NULL,
			latitude float NULL,
			longitude float NULL );

--add primary key
ALTER TABLE OMOP.location ADD CONSTRAINT xpk_location PRIMARY KEY NONCLUSTERED (location_id);

-- add constraints
ALTER TABLE OMOP.location ADD CONSTRAINT fpk_location_country_concept_id FOREIGN KEY (country_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

-- create indices
CREATE CLUSTERED INDEX idx_location_id_1 ON OMOP.location (location_id ASC);


------------ PAYER_PLAN_PERIOD ----------
--HINT DISTRIBUTE ON KEY (person_id)
CREATE TABLE OMOP.PAYER_PLAN_PERIOD (
			payer_plan_period_id integer NOT NULL,
			person_id integer NOT NULL,
			payer_plan_period_start_date date NOT NULL,
			payer_plan_period_end_date date NOT NULL,
			payer_concept_id integer NULL,
			payer_source_value varchar(50) NULL,
			payer_source_concept_id integer NULL,
			plan_concept_id integer NULL,
			plan_source_value varchar(50) NULL,
			plan_source_concept_id integer NULL,
			sponsor_concept_id integer NULL,
			sponsor_source_value varchar(50) NULL,
			sponsor_source_concept_id integer NULL,
			family_source_value varchar(50) NULL,
			stop_reason_concept_id integer NULL,
			stop_reason_source_value varchar(50) NULL,
			stop_reason_source_concept_id integer NULL );

-- add primary key
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT xpk_payer_plan_period PRIMARY KEY NONCLUSTERED (payer_plan_period_id);


-- add constraints
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_person_id FOREIGN KEY (person_id) REFERENCES OMOP.PERSON (PERSON_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_payer_concept_id FOREIGN KEY (payer_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_payer_source_concept_id FOREIGN KEY (payer_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_plan_concept_id FOREIGN KEY (plan_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_plan_source_concept_id FOREIGN KEY (plan_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_sponsor_concept_id FOREIGN KEY (sponsor_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_sponsor_source_concept_id FOREIGN KEY (sponsor_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_stop_reason_concept_id FOREIGN KEY (stop_reason_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.payer_plan_period ADD CONSTRAINT fpk_payer_plan_period_stop_reason_source_concept_id FOREIGN KEY (stop_reason_source_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);


-- create indices
CREATE CLUSTERED INDEX idx_period_person_id_1 ON OMOP.payer_plan_period (person_id ASC);


---------- SPECIMEN ---------------
--HINT DISTRIBUTE ON KEY (person_id)
CREATE TABLE OMOP.SPECIMEN (
			specimen_id integer NOT NULL,
			person_id integer NOT NULL,
			specimen_concept_id integer NOT NULL,
			specimen_type_concept_id integer NOT NULL,
			specimen_date date NOT NULL,
			specimen_datetime datetime NULL,
			quantity float NULL,
			unit_concept_id integer NULL,
			anatomic_site_concept_id integer NULL,
			disease_status_concept_id integer NULL,
			specimen_source_id varchar(50) NULL,
			specimen_source_value varchar(50) NULL,
			unit_source_value varchar(50) NULL,
			anatomic_site_source_value varchar(50) NULL,
			disease_status_source_value varchar(50) NULL );

-- add primary key
ALTER TABLE OMOP.SPECIMEN ADD CONSTRAINT xpk_specimen PRIMARY KEY NONCLUSTERED (specimen_id);


-- add constraints
ALTER TABLE OMOP.specimen ADD CONSTRAINT fpk_specimen_person_id FOREIGN KEY (person_id) REFERENCES OMOP.PERSON (PERSON_ID);
ALTER TABLE OMOP.specimen ADD CONSTRAINT fpk_specimen_specimen_concept_id FOREIGN KEY (specimen_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.specimen ADD CONSTRAINT fpk_specimen_specimen_type_concept_id FOREIGN KEY (specimen_type_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.specimen ADD CONSTRAINT fpk_specimen_unit_concept_id FOREIGN KEY (unit_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.specimen ADD CONSTRAINT fpk_specimen_anatomic_site_concept_id FOREIGN KEY (anatomic_site_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);
ALTER TABLE OMOP.specimen ADD CONSTRAINT fpk_specimen_disease_status_concept_id FOREIGN KEY (disease_status_concept_id) REFERENCES OMOP.CONCEPT (CONCEPT_ID);

-- create indices
CREATE CLUSTERED INDEX idx_specimen_person_id_1 ON OMOP.specimen (person_id ASC);
CREATE INDEX idx_specimen_concept_id_1 ON OMOP.specimen (specimen_concept_id ASC);