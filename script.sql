create table Users (
    id int GENERATED ALWAYS AS IDENTITY primary key,
    login varchar(30) unique,
    password varchar(30),
    role varchar(20)
);

create table Meetings (
    id int GENERATED ALWAYS AS IDENTITY primary key,
    creator_id int references Users(id),
    secretary_id int references Users(id),
    theme varchar(255)
);

create table Question (
    id int GENERATED ALWAYS AS IDENTITY primary key,
    meeting_id int references Meetings(id),
    question_text varchar(255),
    responder_id int references Users(id),
    file varchar(255)
);

create table Calendar (
    meeting_id int references Meetings(id),
    date date,
    time time,
    duration time
);

create table Participant
(
    id            integer generated always as identity
        primary key,
    meeting_id    integer
        references meetings,
    id_from_users integer
        references users,
    status        varchar(20) default 'invited'::character varying
);

create table Creator (
    id int GENERATED ALWAYS AS IDENTITY primary key,
    meeting_id int references Meetings(id),
    id_from_users int references Users(id)
);

create table Guest (
    id int GENERATED ALWAYS AS IDENTITY primary key,
    meeting_id int references Meetings(id),
    id_from_users int references Users(id)
);

create table invitations
(
    id          serial
        primary key,
    meeting_id  integer
        references meetings,
    user_id     integer
        references users,
    status      varchar(20) default 'invited'::character varying,
    invite_date timestamp   default CURRENT_TIMESTAMP
);

