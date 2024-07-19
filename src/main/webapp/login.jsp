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
    <title>Login</title>
</head>
<body>
<%
    try {
        if (session.getAttribute("LOGGED_IN") == null || !(Boolean) session.getAttribute("LOGGED_IN")) {
            ApplicationDB db = new ApplicationDB();
            Connection con = db.getConnection();
            Statement stmt = con.createStatement();

            // Get parameters from HTML form
            String username = request.getParameter("username");
            String password = request.getParameter("password");

            String getPassword = "SELECT * FROM users WHERE username = '" + username + "' AND pass = '" + password + "';";
            ResultSet rs = stmt.executeQuery(getPassword);

            if (rs.next()) {
                String correctPassword = rs.getString(2);

                if (correctPassword.equals(password)) {
                    session.setAttribute("LOGGED_IN", true);
                }

                String getCustomer = "SELECT * FROM customer WHERE username = '" + username + "';";
                rs = stmt.executeQuery(getCustomer);
                if (rs.next()) {
                    session.setAttribute("USER_TYPE", "customer");
                    response.sendRedirect("/cs336_war_exploded/main.jsp");
                } else {
                    // if not a customer, check if they are a service representative
                    String getService = "SELECT * FROM service WHERE username = '" + username + "';";
                    rs = stmt.executeQuery(getService);
                    if (rs.next()) {
                        session.setAttribute("USER_TYPE", "service");
                        response.sendRedirect("/cs336_war_exploded/service.jsp");
                    }
                    // if user is not a customer or a service rep, they must be a manager
                    else {
                        session.setAttribute("USER_TYPE", "manager");
                        response.sendRedirect("/cs336_war_exploded/main.jsp");
                    }
                }

                //Close the connection. Don't forget to do it, otherwise you're keeping the resources of the server allocated.
                con.close();

            }
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
%>
<main class="max-w-[800px] mx-auto">
    <div>
        <h1 class="title">Login</h1>
        <div>
            <form class="flex flex-col gap-10" method="post" action="login.jsp" name="username">
                <label class="flex flex-col">Username
                    <input type="text" class="h-10 rounded-xl border-2 border-blue-400">
                </label>
                <label class="flex flex-col">Password
                    <input type="password" class="h-10 rounded-xl border-2 border-blue-400" name="password">
                </label>
                <button type="submit" class="bg-blue-400 h-10 rounded-xl">Login</button>
            </form>
        </div>
    </div>
</main>
</body>
</html>
