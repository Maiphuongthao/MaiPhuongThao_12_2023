USE epic_events;

INSERT INTO departments (`name`)
VALUES
    ('Gestion'),
    ('Commercial'),
    ('Support');

INSERT INTO permissions (`department_id`,`ob_name`, `ob_action`, `ob_type`, `ob_field`)
VALUES
    (1,'employee', 'create', 'na', 'all'),
    (1,'employee', 'update', 'all', 'all'),
    (1,'employee', 'delete', 'all', 'na'),
    (1,'contract', 'create', 'na', 'all'),
    (1,'contract', 'update', 'no_signature', 'all'),
    (1,'event', 'update', 'all', 'support_id'),
    (1,'event', 'read_no_support', 'no_support', 'na'),
    (2,'client', 'create', 'na', 'all'),
    (2,'client', 'update', 'na', 'all'),
    (2,'contract', 'update', 'owned', 'status'),
    (2,'contract', 'read_no_signature', 'no_signature', 'na'),
    (2,'contract', 'read_due_amount', 'due_amount', 'na'),
    (2,'event', 'create', 'na', 'all'),
    (2,'event', 'update', 'owned', 'all'),
    (3,'event', 'update', 'owned', 'note'),
    (3,'event', 'read_owned', 'owned', 'na'),
    (1,'event', 'read_all', 'all', 'na'),
    (2,'event', 'read_all', 'all', 'na'),
    (3,'event', 'read_all', 'all', 'na'),
    (1,'employee', 'read_all', 'all', 'all'),
    (2,'employee', 'read_all', 'all', 'all'),
    (3,'employee', 'read_all', 'all', 'all'),
    (1,'contract', 'read_all', 'all', 'all'),
    (2,'contract', 'read_all', 'all', 'all'),
    (3,'contract', 'read_all', 'all', 'all'),
    (1,'event', 'read_one', 'all', 'all'),
    (2,'event', 'read_one', 'all', 'all'),
    (3,'event', 'read_one', 'all', 'all'),
    (1,'employee', 'read_one', 'all', 'all'),
    (2,'employee', 'read_one', 'all', 'all'),
    (3,'employee', 'read_one', 'all', 'all'),
    (1,'contract', 'read_one', 'all', 'all'),
    (2,'contract', 'read_one', 'all', 'all'),
    (3,'contract', 'read_one', 'all', 'all');


INSERT INTO employees (`name`, `email`, `password`, `department_id`)
VALUES
    ('Lucie Page', 'lucie@test.com','$argon2id$v=19$m=16,t=2,p=1$QmQ2VjZ1SEZGNVdteVVwaA$45lep5zDs1oJYdG66alo3w', 1),
    ('Benjamin Button', 'ben@test.com','$argon2id$v=19$m=16,t=2,p=1$QmQ2VjZ1SEZGNVdteVVwaA$45lep5zDs1oJYdG66alo3w', 2),
    ('Lao Nguyen', 'lao@test.com','$argon2id$v=19$m=16,t=2,p=1$QmQ2VjZ1SEZGNVdteVVwaA$45lep5zDs1oJYdG66alo3w', 3);
    
INSERT INTO clients (`name`, `email`, `telephone`, `company_name`, `commercial_id`)
VALUES
    ('first client', 'client1@test.com', '0612345678', 'company1', 1);

INSERT INTO contracts (`client_id`, `commercial_id`, `total_amount`, `due_amount`, `status`)
VALUES
    (1, 2, 100.00, 50.00, 'signé'),
    (1, 2, 200.00, 200.00, 'en attend');

INSERT INTO events (`contract_id`, `client_id`, `start_date`, `end_date`, `support_id`, `location`, `total_attendees`, `notes`)
VALUES
    (1, 1, '01/01/2023', '01/10/2023', 3, 'Paris', 50, null),
    (2, 1, '02/10/2023', '08/10/2023', null, 'Paris', 50, null);