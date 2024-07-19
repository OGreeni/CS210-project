<%--
  Created by IntelliJ IDEA.
  User: ogreeni
  Date: 7/19/24
  Time: 4:13 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Reservations</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
<nav class="bg-blue-400 flex justify-center gap-10 h-10 items-center text-xl rounded-b-xl mb-10">
    <form method="post" action="logout.jsp">
        <button class="mt-4">Logout</button>
    </form>
    <form method="post" action="main.jsp">
        <button class="mt-4">Main</button>
    </form>
</nav>
<main class="max-w-[1000px] mx-auto">
    <h2 class="text-2xl">Current reservations</h2>
    <!--TODO: query list of reservations for customer. Click to cancel.-->
    <div class="flex flex-col gap-5">
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Cancel reservation</button>
        </div>
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Cancel reservation</button>
        </div>
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
            <button class="rounded-xl b-2 bg-blue-400 p-2">Cancel reservation</button>
        </div>
    </div>

    <h2 class="text-2xl">Past reservations</h2>
    <!--TODO: query list of reservations for customer.-->
    <div class="flex flex-col gap-5">
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
        </div>
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
        </div>
        <div class="rounded-xl border-2 border-blue-400 p-2 text-left">
            <p>Stops: 10</p>
            <p>Fare: $100</p>
        </div>
    </div>
</main>
</body>
</html>
