<%@ page import="com.example.cs336.ApplicationDB" %>
<%@ page import="java.sql.Statement" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="javax.xml.transform.Result" %>
<%@ page import="java.sql.ResultSet" %><%--
  Created by IntelliJ IDEA.
  User: ogreeni
  Date: 7/19/24
  Time: 4:11 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Main</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<nav class="bg-blue-400 flex justify-center gap-10 h-10 items-center text-xl rounded-b-xl mb-10">
    <form method="post" action="logout.jsp">
        <button class="mt-4">Logout</button>
    </form>
    <form method="post" action="reservations.jsp">
        <button class="mt-4">Reservations</button>
    </form>
</nav>
<body>
<main class="max-w-[1000px] mx-auto">
    <h1 class="text-3xl text-center">Search train schedules</h1>
    <!--TODO: on submit, search for schedules-->
    <form class="flex flex-col gap-10" action="main.jsp" method="post">
        <label class="flex flex-col">Origin (station ID)
            <input type="text" class="h-10 rounded-xl border-2 border-blue-400" name="origin">
        </label>
        <label class="flex flex-col">Destination
            <input type="text" class="h-10 rounded-xl border-2 border-blue-400" name="destination">
        </label>
        <label class="flex flex-col">Date
            <input type="date" class="h-10 rounded-xl border-2 border-blue-400" name="date">
        </label>
        <div>
            <p>Sort by</p>
            <input type="radio" id="arrival" name="sort" value="arrival" checked>
            <label for="arrival">Arrival time</label><br>
            <input type="radio" id="departure" name="sort" value="departure">
            <label for="departure">Departure time</label><br>
            <input type="radio" id="fare" name="sort" value="fare">
            <label for="fare">Fare</label>
        </div>

        <button type="submit" class="bg-blue-400 h-10 rounded-xl">Search</button>
    </form>

    <%
        ApplicationDB db = new ApplicationDB();
        Connection con = db.getConnection();
        Statement stmt = con.createStatement();


        String sort = request.getParameter("sort");
        String origin = request.getParameter("origin");
        String destination = request.getParameter("destination");
        String date = request.getParameter("date");

        if (sort != null && origin != null && destination != null && date != null) {
            String getTrainSchedules = "SELECT * FROM routes \n" +
                    "JOIN (SELECT *, ADDTIME(s.departure, r.travel_time) AS arrival FROM schedule AS s JOIN routes AS r USING (line)) AS full_sched USING (line)\n" +
                    " WHERE line IN (SELECT line FROM routes r JOIN stops s USING (line) WHERE s.stid =" + origin + "\n" +
                    "    AND r.line IN (SELECT line FROM routes JOIN stops USING (line) WHERE stid = " + destination + ")\n" +
                    "    AND stop < (SELECT stop FROM routes JOIN stops USING (line) WHERE line = r.line AND stid = " + destination + "))\n" +
                    "    AND DATE(departure) = '" + date + "' ORDER BY " + sort + ";\n";

            ResultSet rs = stmt.executeQuery(getTrainSchedules);
            while (rs != null && rs.next()) {
                out.print("  <div class=\"rounded-xl border-2 border-blue-400 p-2 text-left\">\n" +
                        "            <p>Stops: 10</p>\n" +
                        "            <p>Fare: $100</p>\n" +
                        "            <button class=\"rounded-xl b-2 bg-blue-400 p-2\">Purchase one way</button>\n" +
                        "            <button class=\"rounded-xl b-2 bg-blue-400 p-2\">Purchase round trip</button>\n" +
                        "        </div>");
            }
        }

    %>
    <div class="flex flex-col gap-5">
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Purchase one way</button>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Purchase round trip</button>
        </div>
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Purchase one way</button>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Purchase round trip</button>
        </div>
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Purchase one way</button>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Purchase round trip</button>
        </div>
    </div>
</main>
</body>
</html>
