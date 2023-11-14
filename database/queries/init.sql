DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users') THEN
        CREATE TYPE role_enum AS ENUM ('doctor', 'patient', 'admin');
        CREATE TABLE users (
            username VARCHAR PRIMARY KEY,
            name VARCHAR,
            role role_enum,
            password VARCHAR
        );
        INSERT INTO users(username, name, role, password) VALUES ('admin', 'admin', 'admin', 'admin');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'medicine') THEN
        CREATE TEMPORARY TABLE temp_medicine (
            name VARCHAR,
            brand VARCHAR,
            type VARCHAR,
            composition VARCHAR,
            price REAL,
            prescription VARCHAR
        );

        CREATE TABLE medicine (
            name VARCHAR,
            brand VARCHAR,
            type VARCHAR,
            composition VARCHAR,
            price REAL,
            prescription BOOLEAN DEFAULT false,
            PRIMARY KEY (name, brand, type, composition)
        );
        
        COPY temp_medicine(name, brand, type, composition, price, prescription) FROM '/docker-entrypoint-initdb.d/all_medicines.csv' DELIMITER ',' CSV HEADER;

        INSERT INTO medicine (name, brand, type, composition, price, prescription)
        SELECT DISTINCT
            temp_medicine.name,
            temp_medicine.brand,
            temp_medicine.type,
            temp_medicine.composition,
            temp_medicine.price,
            CASE
                WHEN temp_medicine.prescription = 'Prescription Required' THEN true
                ELSE false
            END AS prescription
        FROM temp_medicine ON CONFLICT (name, brand, type, composition) DO NOTHING;
        
        DROP TABLE IF EXISTS temp_medicine;
    END IF;
END $$;
