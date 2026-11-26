-- Runs once, on first creation of the data volume.
-- Table schemas come later via migrations; this only enables extensions.
CREATE EXTENSION IF NOT EXISTS vector;