import os
import multiprocessing as mp

NUM_PARALLEL_DOWNLOADS = 20
INPUT_LIST = 'inputs-list.txt'
TEMP_DIR = 'staging'
FINAL_DIR = 'output-files'

def process_url(q, url):
  fn = url.split('/')[-1]
  if os.path.isfile(os.path.join(FINAL_DIR, fn)):
    return
  else:
    q.put((url, fn))

def downloader(q):
  while True:
    item = q.get(True)
    if item is None:
        return
    url, fn = item
    download_and_check(url, fn)

def execute_cmd(cmd):
  #cmd = f'echo {cmd}'
  print(f'START: {cmd}')
  rc = os.system(cmd)
  if rc == 0:
    print(f'FINISH: {cmd}')
    return True
  print(f'FAILURE: {cmd} rc={rc}')
  return False


def download_and_check(url, fn):
  in_path = os.path.join(TEMP_DIR, fn)
  out_path = os.path.join(FINAL_DIR, fn)
  cmd = f'gsutil -u silicon-current-319805 cp {url} {TEMP_DIR}'
  if not execute_cmd(cmd):
    return
  if check(in_path):
    cmd = f'mv {in_path} {out_path}'
    execute_cmd(cmd)

def check(fn):
  cmd = f'tar -tf {fn} > /dev/null'
  return execute_cmd(cmd)



def main():
  os.makedirs(TEMP_DIR, exist_ok=True)
  os.makedirs(FINAL_DIR, exist_ok=True)

  q = mp.Queue()
  p = mp.Pool(NUM_PARALLEL_DOWNLOADS, downloader, (q,))
  with open(INPUT_LIST) as input_f:
    while True:
      url = input_f.readline()
      if not url:
        break
      else:
        process_url(q, url.strip())

  for _ in range(NUM_PARALLEL_DOWNLOADS):
    q.put(None)
  q.close()
  q.join_thread()
  p.close()
  p.join()

if __name__ == '__main__':
  main()