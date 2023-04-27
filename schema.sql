CREATE TABLE Person (
    person_id   SERIAL       NOT NULL,
    user_name VARCHAR(50)  NOT NULL,
    bio       VARCHAR(255) NOT NULL,
    email     VARCHAR(50)  NOT NULL,
    "password"  VARCHAR(255)  NOT NULL,
    university VARCHAR(50) NOT NULL,
    PRIMARY KEY (person_id)
);

CREATE TABLE Section (
    section_id  SERIAL      NOT NULL,
    title       VARCHAR(50) NOT NULL,
    description TEXT ,
    university  VARCHAR(50) NOT NULL,
    course      VARCHAR(50) NOT NULL,
    main        BOOLEAN,
    PRIMARY KEY (section_id)
);

CREATE TABLE person_section (
    person   INT NOT NULL,
    course INT NOT NULL,
    FOREIGN KEY (person) REFERENCES Person(person_id),
    FOREIGN KEY (course) REFERENCES section(section_id)
);

CREATE TABLE user_following (
    follower INT NOT NULL,
    followee INT NOT NULL,
    FOREIGN KEY (follower) REFERENCES Person(person_id),
    FOREIGN KEY (followee) REFERENCES Person(person_id)
);

CREATE TABLE Post (
    post_id     SERIAL    NOT NULL,
    poster      INT       NOT NULL,
    course      INT       NOT NULL,
    date_time   TIMESTAMP NOT NULL,
    content     TEXT      NOT NULL,
    parent_post INT,
    PRIMARY KEY (post_id),
    FOREIGN KEY (poster) REFERENCES Person(person_id),
    FOREIGN KEY (course) REFERENCES Section(section_id)
);