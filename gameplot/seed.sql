INSERT INTO games (name, description, steam_url, itch_url) VALUES
    ('Glumbo''s Adventure', 'Incredibly Epic', '', ''),
    ('Stardew Valley', 'Makes u gay', 'https://store.steampowered.com/app/413150/Stardew_Valley/', '')
    ;

INSERT INTO jobs (payload, status, worker_id, insert_ts, pickup_ts, completion_ts, result) VALUES
    ('{"name": "foo1", "args": []}', 'pending', NULL, '11/5/2025', NULL, NULL, NULL),
    ('{"name": "foo2", "args": []}', 'active', NULL, '11/5/2025', NULL, NULL, NULL),
    ('{"name": "foo3", "args": []}', 'active', 'asdjhfkl33sdh98', '11/5/2025', NULL, NULL, NULL),
    ('{"name": "foo4", "args": []}', 'done', NULL, '11/5/2025', NULL, NULL, NULL),
    ('{"name": "foo5", "args": []}', 'errored', NULL, '11/5/2025', NULL, NULL, NULL),
    ('{"name": "foo6", "args": []}', 'pending', 'asdfasdljkhas4df', '11/4/2025', NULL, NULL, NULL),
    ('{"name": "test", "args": [1,2,3]}', 'pending', 'asdfasdljkhas4df', '11/4/2025', NULL, NULL, NULL)
    ;

INSERT INTO users (email, password) VALUES
    ('example@poopoo.com', 'asdfg'),
    ('admin@doodoo.com', 'scrypt:32768:8:1$qSRVmEJHCLpgeRPP$44b1a5b52fd8185ffa04b35ec3b5abd4bb7af1933ed1cd885f83e2a8fb298b6fb5bdec26e15e5ea7b9e7ff66581a67f1841d11c59f56138a0e41d00eae74cd56')
    ;
-- admin@doodoo.com & password 