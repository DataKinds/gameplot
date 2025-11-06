INSERT INTO games (name, description, steam_url, itch_url) VALUES
    ('Glumbo''s Adventure', 'Incredibly Epic', '', ''),
    ('Stardew Valley', 'Makes u gay', 'https://store.steampowered.com/app/413150/Stardew_Valley/', '')
    ;

INSERT INTO jobs (payload, status, worker_id, insert_ts, pickup_ts, completion_ts, result) VALUES
    ('"foo1"', 'pending', NULL, '11/5/2025', NULL, NULL, NULL),
    ('"foo2"', 'active', NULL, '11/5/2025', NULL, NULL, NULL),
    ('"foo8"', 'active', 'asdjhfkl33sdh98', '11/5/2025', NULL, NULL, NULL),
    ('"foo3"', 'done', NULL, '11/5/2025', NULL, NULL, NULL),
    ('"foo4"', 'errored', NULL, '11/5/2025', NULL, NULL, NULL),
    ('"foo5"', 'pending', 'asdfasdljkhas4df', '11/4/2025', NULL, NULL, NULL)
    ;
