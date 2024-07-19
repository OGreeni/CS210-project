<%@ page import="com.example.cs336.ApplicationDB" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.Statement" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page import="java.sql.SQLException" %><%--
  Created by IntelliJ IDEA.
  User: ogreeni
  Date: 7/19/24
  Time: 12:58 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<script src="https://cdn.tailwindcss.com"></script>
<html>
<head>
    <title>Register</title>
</head>
<body>
<%
    ApplicationDB db = new ApplicationDB();
    Connection conn = db.getConnection();
    Statement stmt = conn.createStatement();

    String username = request.getParameter("username");
    String firstName = request.getParameter("first_name");
    String lastName = request.getParameter("last_name");
    String password = request.getParameter("password");

    if (username != null) {
        String saveUser = "INSERT into Users VALUES ('" + username + "','" + firstName + "','" + lastName + "','" + password + "');";
        stmt.executeUpdate(saveUser);
        response.sendRedirect("/cs336_war_exploded/main.jsp");
    }
%>
<main class="max-w-[800px] mx-auto">
    <div>
        <h1 class="title">Register your account</h1>
        <div>
            <form class="flex flex-col gap-10" method="post" action="register.jsp">
                <label class="flex flex-col">Username
                    <input type="text" class="h-10 rounded-xl border-2 border-blue-400" name="username">
                </label>
                <label class="flex flex-col">First name
                    <input type="text" class="h-10 rounded-xl border-2 border-blue-400" name="first_name">
                </label>
                <label class="flex flex-col">Last name
                    <input type="text" class="h-10 rounded-xl border-2 border-blue-400" name="last_name">
                </label>
                <label class="flex flex-col">Password
                    <input type="password" class="h-10 rounded-xl border-2 border-blue-400" name="password">
                </label>
                <button type="submit" class="bg-blue-400 h-10 rounded-xl">Register</button>
            </form>
        </div>
    </div>
</main>
</body>
</html>
