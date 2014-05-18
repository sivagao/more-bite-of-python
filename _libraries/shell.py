
### Info
# https://github.com/houqp/shell.py/blob/master/shell/parallel_exec.py


### 基础库
from subprocess import Popen
from subprocess import PIPE

class subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)


subprocess.PIPE
Special value that can be used as the stdin, stdout or stderr argument to Popen and indicates that a pipe to the standard stream should be opened.

Popen.communicate(input=None)
Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate. 
communicate() returns a tuple (stdoutdata, stderrdata).
Note that if you want to send data to the process’s stdin, you need to create the Popen object with stdin=PIPE.
Similarly, to get anything other than None in the result tuple, you need to give stdout=PIPE and/or stderr=PIPE too.


### Usage

# block until return
from shell import ex
ex('echo hollo|grep hello').stdout()
# string output with \n

# asynchronous execution
from shell import asex
c = asex('<async op cmd>')
c.stdout() # wait unitl process exit and read stdout

# pipe commands
from shell import ex
re = (ex('ifconfig') 
	| 'grep -A 1 etho0' 
	| 'grep inet' 
	| 'awk "{print $2}"' 
	| 'cut -d: -f 2').stdout()

# p -> pipe
ex('echo 1 3 5').p('awk "{print $1}"').stdout()


# or another way
from shell import pipe_all
pipe_all(['ls -la !',
	'awk "{print $9}"',
	'grep -E "^\."',
	'wc -l']).stdout()

# use string as stdin
instream('1 2 4').p('awk "{print $1}"').stdout()

# or using pipe instream
ex('echo 1 3 5').p('awk "{print $1}"').stdout()


# run commands in parallel
from shell import parallel as par
par.ex_all(['sleep 2', 'sleep 2']) 3 # return in 2s

# async parallel execution
pe = par.asex_all(['sleep 2', 'sleep 2'])
pe.wait()

# set working directory
with shell.cwd('~/server/data/upload') as old_path:
	shell.ex('find ./images -name *.png') | 'minify ./public' >> 'upload.log'

# equivalent to
shell.ex('find ~/server/data/upload/images -name "*.png"') | 'minify ~/server/data/upload/public' >> '~/server/data/upload.log'


# api.py

def ex(cmd_str):
	return RunCmd(cmd_str).wait()

def asex(cmd_str):
	return RunCmd(cmd_str).init_popen()

def pipe_all(cmd_lst):
	ssr = RunCmd(cmd_lst.pop(0))
	for cmd in cmd_lst:
		ssr = ssr.p(cmd)
	return ssr

def p(arg):
	if isinstance(arg, basestring):
		return RunCmd(arg)
	elif isinstance(arg, list):
		return pipe_all(arg)
	else:
		raise ValueError('argument must be a string or list')

@contextmanager
def cwd(new_dir):
	"""
	used with with, temporarily change the current working directory
	"""
	saved_cwd = os.getcwd()
	os.chdir(os.path.expanduser(new_dir))
	try:
		yield saved_cwd
	finally:
		os.chdir(saved_cwd)


# run_cmd.py

class RunCmd():
	def __init__(self, cmd_str, input_pipe=None):
		self.cmd_str = cmd_str
		self.cmd_p = None
		if input_pipe:
			self.input_pipe = input_pipe
		else:
			self.input_pipe = None
		self.std = {'out': None, 'err': None}

	def get_cmd_list(self):
		pass

	def init_popen(self):
		if self.cmd_p is None:
			self.cmd_p = Popen(
				self.get_cmd_list(),
				stdin=self.input_pipe, stdout=PIPE, stderr=PIPE
			)
		return self

	def get_popen(self):
		return self.init_popen().cmd_p

	def p(self, cmd):
		in_pipe = None
		if self.std['out']:
			in_pipe = str_to_pipe(self.std['out'])
		else:
			cmd_p = self.get_popen()
			in_pipe = cmd_p.stdout
		return RunCmd(cmd, input_pipe=in_pipe)


	def stdout(self):
		if self.std['out'] is None:
			self.wait()
		return self.std['out']

	def __or__(self, other):
		if isinstance(other, basestring):
			return self.p(other)
		elif isinstance(other, RunCmd):
			return self.p(other.cmd_str)
		raise ValueError('argument must be a string or an instance of RunCmd')

	def __gt__(self, target):
		self.wr(target)

	def __rshift__(self, target):
		self.ap(target)

# input_stream
class InputStream():
	def __init__(self, input_str):
		self.input_pipe = str_to_pipe(input_str)

	def p(self, cmd):
		return RunCmd(cmd, input_pipe=self.input_pipe)

# parallel_exec
class ParallelExec:
	def __init__(self, cmd_str_list):
		pass

# util.py
import tempfile

def check_attrs(obj, attr_list):
	return all([ hasattr(obj, attr) for atrr in attr_list])

def str_to_pipe(s):
	# 本质上构造一个类pipe(file)的monkey type
	input_pipe = tempfile.SpooledTemporaryFile()
	input_pipe.write(s)
	input_pipe.seek(0)
	return input_pipe



