DROP DATABASE IF EXISTS Predicted_outputs;

CREATE DATABASE IF NOT EXISTS Predicted_outputs;

USE Predicted_outputs;

CREATE TABLE predicted_outputs
(
	Reason_Group_1 BIT NOT NULL,
    Reason_Group_2 BIT NOT NULL,
    Reason_Group_3 BIT NOT NULL,
    Reason_Group_4 BIT NOT NULL,
    Month_value INT NOT NULL,
    Transportation_Expense INT NOT NULL,
    Age INT NOT NULL,
    Boday_Mass_Index INT NOT NULL,
    Education BIT NOT NULL,
    Children INT NOT NULL,
    Pets INT NOT NULL,
    Probability FLOAT NOT NULL,
    Prediction BIT NOT NULL
);

SELECT * FROM predicted_outputs;