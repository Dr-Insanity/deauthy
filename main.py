import time
from typing import Union
from deauthy.auto_installer import Dependencies
from deauthy.functs import mod_config, del_pair, get_var
if get_var('not_setup_yet'):
    Dependencies.installed()
    del_pair('not_setup_yet')
from socket import if_nameindex
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from sys import exit
from halo import Halo
from deauthy.deauthy_types import BSSID, ESSID, Interface
from deauthy.terminal import Terminal
from deauthy.checks import Checks
from deauthy.functs import Functs
import threading

def version():
    with open('deauthy/VERSION', 'r') as f:
        v = f.readline()
        f.close()
        return v

red         = Terminal.Red
cyan        = Terminal.Cyan
blue        = Terminal.Blue
white       = Terminal.White
bold        = Terminal.Bold
yellow      = Terminal.Yellow
light_green = Terminal.Light_green
light_white = Terminal.Light_white
end         = Terminal.End
light_blue  = Terminal.Light_blue
underline   = Terminal.Underline

def clear():
    check_call(["clear"])

class Banner:
    busy = False
    delay = 0.1
    frame1 = f"""{cyan}*   {blue}°     {cyan}*      {cyan}*    {blue}°      {cyan}*    {blue}°     {cyan}*      {cyan}*    {blue}°   {cyan}*   {blue}°   {cyan}*
.  {cyan}*    {blue}°   {cyan}*    {blue}°    {blue}°     {cyan}* {blue}°          {cyan}*         {blue}° {cyan}*   {blue}°  {cyan}*     {blue}°  .
.    {red}██████╗ ███████╗     █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗ {blue}°
   {blue}° {red}██╔══██╗██╔════╝    ██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝ {cyan}* {blue}°
{cyan}*    {red}██║  ██║█████╗█████╗███████║██║   ██║   ██║   ███████║ ╚████╔╝  {blue}°
{blue}° {blue}°  {red}██║  ██║██╔══╝╚════╝██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝   {cyan}* {blue}°
{cyan}*    {red}██████╔╝███████╗    ██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║    {blue}°
{blue}°  {blue}° {red}╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝  {blue}°
 {blue}°     {cyan}*  {blue}°   {cyan}* {blue}°         {cyan}*          {blue}° {cyan}*     {blue}°    {blue}°    {cyan}*   {blue}°    {cyan}*  .
    {cyan}*   {blue}°     {cyan}*      {cyan}*    {blue}°      {cyan}*    {blue}°     {cyan}*      {cyan}*    {blue}°   {cyan}*   {blue}°   {cyan}*{end}"""

    frame2 = f"""{blue}°   {cyan}*     {blue}°      {blue}°    {cyan}*      {blue}°    {cyan}*     {blue}°      {blue}°    {cyan}*   {blue}°   {cyan}*   {blue}°
{cyan}*  {blue}°    {cyan}*   {blue}°    {cyan}*    {cyan}*     {blue}° {cyan}*          {blue}°         {cyan}* {blue}°   {cyan}*  {blue}°     {cyan}*  {cyan}*
{cyan}*    {red}██████╗ ███████╗     █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗ {cyan}*
   {cyan}* {red}██╔══██╗██╔════╝    ██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝ {blue}° {cyan}*
{blue}°    {red}██║  ██║█████╗█████╗███████║██║   ██║   ██║   ███████║ ╚████╔╝{white}  {cyan}*
{cyan}* {cyan}*  {red}██║  ██║██╔══╝╚════╝██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝{white}   {blue}° {cyan}*
{blue}°    {red}██████╔╝███████╗    ██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║{white}    {cyan}*
{cyan}*  {cyan}* {red}╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝{white}  {cyan}*
 {cyan}*     {blue}°  {cyan}*   {blue}° {cyan}*         {blue}°          {cyan}* {blue}°     {cyan}*    {cyan}*    {blue}°   {cyan}*    {blue}°  {cyan}*
    {blue}°   {cyan}*     {blue}°      {blue}°    {cyan}*      {blue}°    {cyan}*     {blue}°      {blue}°    {cyan}*   {blue}°   {cyan}*   .{end}"""

    def banner_task(self):
        while self.busy:
            clear()
            print(self.frame1)
            time.sleep(0.2)
            clear()
            print(self.frame2)
            time.sleep(0.2)

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.banner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        if exception is not None:
            return False

def main():
    Terminal.inform(msg=f"{bold}{light_green}Hey! {end}{light_white}Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")
    Terminal.inform(msg=f"""{white}Type {light_white}"{white}!help{light_white}"{white} for a list of commands!""")
    if Checks.has_root():
        Terminal.inform(msg=f"{white}Running as {light_green}{bold}Root{end}")
    Terminal.prompt(question=f"{white}deauthy | sh", allowed_replies=["deauthy | sh"])

try:
    if not Checks.has_root():
        Terminal.tell_issue(msg=f"{bold}{red}Run it as root...{end}")
        exit(1)
    clear()
    with Banner():
        time.sleep(5)
    time.sleep(2)
    print(light_green + "Time to kick off some assholes from yer net" + f"\n{white}DeAuthy version: {light_white}{version()}")
    main()
except KeyboardInterrupt:
    quit(0)