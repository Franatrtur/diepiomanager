
import pyautogui
import time, json, webbrowser, os
diepversion = "1.1"

points = 7
allpoints = 7 * 4 + 5
special = "!"

logging = True

presets = {}
selected = None

def update_presets(dolog = False):
	global presets
	try:
		with open("_presets.json", "r") as dt:
			presets = json.load(dt)
		if dolog:
			print(" <Presets reloaded>")
	except:
		print(" <Error loading presets>")

def save_presets():
	try:
		with open("_presets.json", "w") as dt:
			json.dump(presets, dt)
	except:
		print(" <Unable to save presets>")
		if logging:
			print(" presets:\n%s" % json.dumps(presets))

def check_preset(setup, dolog = True):
	valid = type(setup) == str and ((len(setup) < allpoints and setup.isdecimal()) or setup[0].startswith(special))
	if not valid:
		print(" <Invalid preset code detected> ")
		if logging and dolog:
			print(" code: %s\n" % setup)
	return valid

def pybox():
	while True:
		pyinp = input(">>")
		if(pyinp == "py"):
			break
		try:
			exec(pyinp)
		except Exception as e:
			print("<error>" if not logging else "<error>: {}".format(e))

def run_type(setupstr, delay):
	print(" <Running %s>" % (("after %ss" % delay) if delay > 0 else "immidiately"))
	actual = setupstr[1:] if setupstr.startswith(special) else setupstr
	print(" Typing: %s" % actual)
	if(delay):
		time.sleep(delay)
	before = time.time()
	pyautogui.keyDown('u')
	time.sleep(0.05)
	pyautogui.write(actual, interval = 0.02)
	time.sleep(0.05)
	pyautogui.keyUp('u')
	print(" <Done in %ss>" % round(time.time() - before, 3))



def cmd_help():
	print("\n== Diep.io automatic upgrade setup manager ==")
	print("Version: %s" % diepversion)
	print("Author: Franatrtur")
	print("Prefix for special presets: %s" % special)
	print("Master commands:\n  exit = safely end the program\n  py = run python code (type py to exit python console)")
	print("Diep commands:\n  save, create, delete, select, reload, print, run")

def cmd_save():
	global presets
	presetname = input(" Preset name:")
	while check_preset(presetname, False):
		print(" <Preset name cannot be a setup>")
		presetname = input(" Valid preset name:")
	presetsetup = input("Preset setup:")
	if check_preset(presetsetup):
		presets[str(presetname).lower()] = presetsetup

def cmd_reload():
	update_presets(True)

def cmd_create():
	webbrowser.open('file://' + os.path.realpath("create.html"))

def cmd_delete(presetname = ""):
	global presets
	if not presetname:
		print(" <Preset name required>")
	if str(presetname).lower() in presets:
		del presets[str(presetname).lower()]
		print(" <Preset %s deleted>" % presetname)
	elif presetname == "all" and input("Are you sure you want to delete all presets? (y/n)").lower().startswith("y"):
		presets = {}
	else:
		print(" <Preset %s not found>" % presetname)

def cmd_select(presetname = ""):
	global presets, selected
	if not presetname:
		print(" <Preset name required>")
	if str(presetname).lower() in presets:
		selected = presets[str(presetname).lower()]
		print(" <Preset %s selected>" % presetname)
	elif check_preset(presetname, False):
		selected = presetname
		print(" <Unsaved setup (%s) selected>" % presetname)
	else:
		print(" <Preset %s not found>" % presetname)

def cmd_print(presetname = ""):
	global presets, selected
	if not presetname:
		if selected:
			print(" <Printing selected setup>")
			print("  %s" % selected)
		else:
			print(" <No setup selected>")
	elif str(presetname).lower() in presets:
		print(" <Printing preset %s>" % presetname)
		print("  %s" % presets[str(presetname).lower()])
	elif str(presetname).lower() == "all":
		print(" <Printing all presets>")
		for nm, val in presets.items():
			print(" %s: %s" % (nm, val))
	else:
		print(" <Preset %s not found>" % presetname)

def cmd_run(presetname = "", after = "3", doclick = "yes"):
	global selected
	if not doclick.startswith("n"):
		pyautogui.click(0, 200)
	try:
		delay = round(float(after), 3)
		assert delay < 1000 and delay >= 0
	except:
		delay = 3
		print(" <Invalid delay, reverting to 3s>")
		if logging:
			print(" rules: delay (2nd arg) between 0 and 1000")
	if not presetname:
		if selected:
			run_type(selected, delay)
		else:
			print(" <No setup selected>")
	elif str(presetname).lower() in presets:
		run_type(presets[str(presetname).lower()], delay)
	elif check_preset(presetname, False):
		run_type(presetname, delay)
	else:
		print(" <Preset %s not found>" % presetname)

def cmd_reset(presetname = "", after = "3", doclick = "yes"):
	pyautogui.keyDown('u')
	pyautogui.keyUp('u')
	print(" <Key U pressed>")


def main():

	global logging, points, allpoints, presets

	print("\n||===================================%s||" % ("=" * len(diepversion)))
	print("|| DIEP.IO automatic setup manager v%s ||" % diepversion)
	print("||===================================%s||" % ("=" * len(diepversion)))

	update_presets()
	
	while True:

		inp = input("\ncommand: ")

		if inp == "exit":
			save_presets()
			break

		elif inp == "py":
			pybox()
			continue

		cmd = inp.split(" ")[0].lower()
		args = inp.split(" ")[1:]

		if ("cmd_" + cmd) in globals() and callable(globals()["cmd_" + cmd]):
			globals()["cmd_" + cmd](*args)

		else:
			print(" <Command not recognized>")

		save_presets()

if __name__ == "__main__":
	main()