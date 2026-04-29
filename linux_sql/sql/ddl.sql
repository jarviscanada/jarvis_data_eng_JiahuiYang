-- 1.switch to database(not necessary if using -d host_agent)
-- \c host_agent

-- 2.create `host_info` table if not exist
CREATE TABLE IF NOT EXISTS public.host_info (
  id SERIAL NOT NULL,
  hostname VARCHAR NOT NULL,
  cpu_number INT NOT NULL,
  cpu_architecture VARCHAR NOT NULL,
  cpu_model VARCHAR NOT NULL,
  cpu_mhz DOUBLE PRECISION NOT NULL,
  l2_cache INT NOT NULL,
  "timestamp" TIMESTAMP,
  total_mem INT,
  CONSTRAINT host_info_pk PRIMARY KEY (id),
  CONSTRAINT host_info_un UNIQUE (hostname)
);

-- 3.create `host_usage` table if not exist
CREATE TABLE IF NOT EXISTS public.host_usage (
  "timestamp" TIMESTAMP NOT NULL,
  host_id INT NOT NULL,
  memory_free INT4 NOT NULL,
  cpu_idle INT2 NOT NULL,
  cpu_kernel INT2 NOT NULL,
  disk_io INT4 NOT NULL,
  disk_available INT4 NOT NULL,
  CONSTRAINT host_usage_host_info_fk FOREIGN KEY (host_id) REFERENCES host_info(id)
);



