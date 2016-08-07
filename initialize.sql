CREATE TABLE UserTable (
	UserName VARCHAR(30) NOT NULL PRIMARY KEY,
	UserPassword VARCHAR(30) NOT NULL
);

INSERT INTO UserTable (UserName, UserPassword) VALUES 
('User1', 'Password1'),
('User2', 'Password2'),
('User3', 'Password3'),
('User4', 'Password4');

CREATE TABLE ListTable(
	L_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	UserName VARCHAR(30) NOT NULL,
	ListName VARCHAR (50) NOT NULL,
	Content VARCHAR(255) NOT NULL,
	WriteOn DATE NOT NULL,
	DueOn DATE NOT NULL,
	FOREIGN KEY (UserName) REFERENCES UserTable(UserName)
);

INSERT INTO ListTable( UserName, ListName, Content, WriteOn, DueOn) VALUES
('User2','Page1','Assignment 1','2010-1-1','2012-1-2'),
('User2','Page1','Assignment 2','2010-1-1','2012-1-2'),
('User2','Page1','Assignment 3','2010-1-1','2012-1-2'),
('User1','Page2','Assignment 11','2010-1-1','2012-1-2'),
('User1','Page2','Assignment 12','2010-1-1','2012-1-2'),
('User1','Page2','Assignment 13','2010-1-1','2012-1-2'),
('User3','Page30','Project 1','2010-1-1','2012-1-2'),
('User1','Page2','Assignment 1','2010-1-1','2012-1-2'),
('User1','Page2','Assignment 2','2010-1-1','2012-1-2'),
('User1','Page3','Assignment 3','2010-1-1','2012-1-2');

DELIMITER //
CREATE PROCEDURE getUser(UserNameIN VARCHAR(30))
BEGIN
	SELECT UserPassword
	FROM UserTable
	WHERE UserName = UserNameIN;
END//

CREATE PROCEDURE getList(UserNameIN VARCHAR(30))
BEGIN
	SELECT a.ListName, a.Content, a.L_ID, a.WriteOn, a.DueOn
	FROM ListTable a INNER JOIN UserTable b
    ON b.UserName = a.UserName
	WHERE b.UserName = UserNameIN;
END//

CREATE PROCEDURE getContent(UserNameIN VARCHAR(30), ListNameIN varchar(50))
BEGIN
	SELECT a.L_ID, a.Content, a.WriteOn, a.DueOn
	FROM ListTable a INNER JOIN UserTable b
	ON a.UserName = b.UserName
	WHERE b.UserName = UserNameIN AND ListName = ListNameIN;
END//

CREATE PROCEDURE InsertContent(UserNameIN VARCHAR(30), ListNameIN VARCHAR(50), ContentIN VARCHAR(255), WriteOnIN DATE, DueOnIN DATE)
BEGIN
	INSERT INTO ListTable( UserName, ListName, Content, WriteOn, DueOn) VALUES( UserNameIN, ListNameIN, ContentIN, WriteOnIN, DueOnIN);
END//

CREATE PROCEDURE DeleteContent(UserNameIN VARCHAR(30),L_IDIN INT)
BEGIN
	Delete FROM ListTable
	WHERE L_ID = L_IDIN AND UserName = UserNameIN;
END//

DELIMITER ;