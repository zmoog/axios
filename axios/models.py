from dataclasses import dataclass


@dataclass
class Credentials:
    username: str
    password: str
    customer_id: str


@dataclass
class Profile(object):
    customer_id: str
    name: str
    customer_title: str
    customer_name: str


@dataclass
class Grade(object):
    date: str
    subject: str
    kind: str
    value: str
    teacher: str
    target: str = ""
    comment: str = ""
