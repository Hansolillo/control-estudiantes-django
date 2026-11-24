USE estudiante_db;

-- Borrar tablas anteriores
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS email, phone, address, student;
SET FOREIGN_KEY_CHECKS = 1;

-- STUDENT
CREATE TABLE student (
    student_id   INT          NOT NULL AUTO_INCREMENT,
    last_name    VARCHAR(45)  NOT NULL,
    middle_name  VARCHAR(45)  NOT NULL,
    first_name   VARCHAR(45)  NOT NULL,
    gender       ENUM('M','F','O') NOT NULL,
    created_on   DATETIME     NULL,
    updated_on   DATETIME     NULL,
    PRIMARY KEY (student_id),
    INDEX student_last_name_idx (last_name)
) ENGINE = InnoDB;

-- EMAIL
CREATE TABLE email (
    email        VARCHAR(100) NOT NULL,
    student_id   INT          NOT NULL,
    email_type   ENUM('personal','trabajo') NOT NULL,
    updated_on   DATETIME     NULL,
    created_on   DATETIME     NULL,
    PRIMARY KEY (email, student_id),
    INDEX student_email_fk_idx (student_id),
    CONSTRAINT student_email_fk FOREIGN KEY (student_id)
        REFERENCES student (student_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- PHONE
CREATE TABLE phone (
    phone_id     INT          NOT NULL AUTO_INCREMENT,
    student_id   INT          NOT NULL,
    phone        VARCHAR(30)  NOT NULL,
    phone_type   ENUM('celular','casa','trabajo') NOT NULL,
    country_code VARCHAR(5)   NULL,
    area_code    VARCHAR(5)   NULL,
    created_on   DATETIME     NULL,
    updated_on   DATETIME     NULL,
    PRIMARY KEY (phone_id, student_id),
    INDEX student_phone_idx (student_id),
    CONSTRAINT student_phone_fk FOREIGN KEY (student_id)
        REFERENCES student (student_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- ADDRESS
CREATE TABLE address (
    address_id   INT          NOT NULL AUTO_INCREMENT,
    student_id   INT          NOT NULL,
    address_line VARCHAR(100) NULL,
    city         VARCHAR(45)  NULL,
    zip_postcode VARCHAR(45)  NULL,
    state        VARCHAR(45)  NULL,
    PRIMARY KEY (address_id, student_id),
    INDEX address_student_FK_idx (student_id),
    CONSTRAINT address_student_FK FOREIGN KEY (student_id)
        REFERENCES student (student_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- DATOS DE PRUEBA
INSERT INTO student (first_name, last_name, middle_name, gender, created_on, updated_on) VALUES
('Ana', 'García', 'López', 'F', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
('Sofía', 'Hernández', 'Martínez', 'F', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
('Carlos', 'Ramírez', 'Torres', 'M', UTC_TIMESTAMP(), UTC_TIMESTAMP());

INSERT INTO email (email, student_id, email_type, created_on, updated_on) VALUES
('ana.garcia@correo.com', 1, 'personal', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
('sofia.hernandez@correo.com', 2, 'personal', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
('carlos.ramirez@correo.com', 3, 'personal', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
('c.ramirez@empresa.com', 3, 'trabajo', UTC_TIMESTAMP(), UTC_TIMESTAMP());

INSERT INTO phone (student_id, phone, phone_type, country_code, area_code, created_on, updated_on) VALUES
(1, '12345678', 'celular', '52', '81', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
(2, '23456789', 'celular', '52', '81', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
(3, '34567890', 'celular', '52', '81', UTC_TIMESTAMP(), UTC_TIMESTAMP()),
(3, '45678901', 'casa', '52', '81', UTC_TIMESTAMP(), UTC_TIMESTAMP());

INSERT INTO address (student_id, address_line, city, state, zip_postcode) VALUES
(1, 'Av. Constitución 100', 'Monterrey', 'Nuevo León', '64000'),
(2, 'Calle Hidalgo 250', 'San Nicolás de los Garza', 'Nuevo León', '66400'),
(3, 'Av. Vasconcelos 300', 'San Pedro Garza García', 'Nuevo León', '66220');