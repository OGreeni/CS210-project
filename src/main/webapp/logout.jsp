<%--
  Created by IntelliJ IDEA.
  User: ogreeni
  Date: 7/19/24
  Time: 4:03 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    session.setAttribute("LOGGED_IN", false);
    response.sendRedirect("/cs336_war_exploded/login.jsp");
%>
<html>
<head>
    <title>Logout</title>
</head>
<body>

</body>
</html>
