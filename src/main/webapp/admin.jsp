<%@ page import="java.sql.ResultSet" %>
<%@ page import="com.example.cs336.ApplicationDB" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.Statement" %>
<%@ page import="java.sql.SQLException" %><%--
  Created by IntelliJ IDEA.
  User: ogreeni
  Date: 7/19/24
  Time: 3:48 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<script src="https://cdn.tailwindcss.com"></script>
<html>
<head>
    <title>Admin</title>
</head>
<body>
<nav class="bg-blue-400 flex justify-center gap-10 h-10 items-center text-xl rounded-b-xl mb-10">
    <form method="post" action="logout.jsp">
        <button class="mt-4">Logout</button>
    </form>
</nav>
<main class="max-w-[1000px] mx-auto">
    <h1 class="text-3xl text-center">Admin dashboard</h1>
    <div class="my-10">
        <h2 class="text-2xl">Sales report</h2>
        <form class="flex flex-col items-start" method="post" action="admin.jsp">
            <label>
                <input type="month" name="date"/>
            </label>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Generate report</button>
        </form>
        <p>Sales: $
            <%
                String date = request.getParameter("date");
                if (date != null) {
                    String year = date.substring(0, 4);
                    String month = date.substring(5, 7);
                    String generateReport = "SELECT MONTH(date), YEAR(date), SUM(fare) AS total_sales FROM reservation WHERE YEAR(date) = " + year + " AND Month(date) = " + month + " GROUP BY MONTH(date), YEAR(date);";
                    ApplicationDB db = new ApplicationDB();
                    Connection con = db.getConnection();
                    Statement stmt = con.createStatement();

                    ResultSet rs = null;
                    try {
                        rs = stmt.executeQuery(generateReport);
                        // Check if result set is empty
                        if (rs.next()) {
                            out.print(rs.getFloat(3));
                        } else {
                            out.print(0);
                        }
                    } catch (SQLException e) {
                        throw new RuntimeException(e);
                    }


                }


            %></p>
    </div>
    <!--TODO: fetch customer representatives. Allow updates to info.-->
    <div class="my-10">
        <h2 class="text-2xl">Customer representatives</h2>
        <div>
            <div class="rounded-xl border-2 border-blue-400 p-2 text-left flex flex-col items-start gap-2">
                <div>
                    <label>Name</label>
                    <input type="text" class="h-10 rounded-xl border-2 border-blue-400" value="John Doe">
                </div>
                <!--TODO: add other detail here.-->
                <div>
                    <button class="rounded-xl b-2 bg-blue-400 p-2">Update details</button>
                    <button class="rounded-xl b-2 bg-blue-400 p-2">Delete representative</button>
                </div>
            </div>
        </div>
    </div>

    <div class="my-10">
        <h2 class="text-2xl">Reservations</h2>
        <div class="mb-2">
            <p>Generate by</p>
            <form method="post" action="admin.jsp">
                <input type="radio" name="type" value="line" checked>
                <label>Transit line</label><br>
                <input type="radio" name="type" value="customer">
                <label>Customer name</label><br>
                <input type="text" class="h-10 rounded-xl border-2 border-blue-400"
                       placeholder="Transit/customer" name="name">
                <button class="rounded-xl b-2 bg-blue-400 p-2">Get reservations</button>
            </form>
            <%
                String type = request.getParameter("type");
                String name = request.getParameter("name");

                ApplicationDB db = new ApplicationDB();
                Connection con = db.getConnection();
                Statement stmt = con.createStatement();
                ResultSet rs = null;


                if (type != null) {
                    String reservationsByTransit = "CALL res_by_line('" + name + "')";
                    rs = stmt.executeQuery(reservationsByTransit);
                }

                while (rs != null && rs.next()) {
                    out.print("<div> Reservation number: " + rs.getString(1) + "</div>");
                }
            %>

        </div>
    </div>

    <h2 class="text-2xl">Revenue</h2>
    <!--TODO: fetch best customer (most revenue generated).-->
    <p class="text-xl">Best customer: <%
        String generateReport = "SELECT user, SUM(fare) AS total_sales FROM reservation GROUP BY user ORDER BY total_sales DESC LIMIT 1;";
        rs = null;

        rs = stmt.executeQuery(generateReport);
        // Check if result set is empty
        if (rs.next()) {
            out.print(rs.getString(1));
        } else {
            out.print(0);
        }
    %></p>
    <!--TODO: fetch 5 most active transit lines.-->
    <p class="text-xl">Most active transit lines:
        <%
            String activeTransitLines = "SELECT line FROM (SELECT line, COUNT(number) res_count FROM routes LEFT JOIN reservation USING (line) GROUP BY line ORDER BY res_count DESC) AS temp LIMIT 5;";
            rs = stmt.executeQuery(activeTransitLines);
            // Check if result set is empty
            while (rs.next()) {
                out.print(rs.getString(1) + ", ");
            }

        %></p>
</main>
</body>
</html>
