<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Service Unavailable</title>
    <style>
        body {
            background-color: #202124; /* Warna background dark mode Chrome */
            color: #bdc1c6; /* Warna teks abu-abu terang */
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
            flex-direction: column;
        }
        .icon {
            width: 56px;
            height: 56px;
            fill: #5f6368; /* Warna ikon abu-abu gelap */
            margin-bottom: 24px;
        }
        .title {
            color: #e8eaed; /* Warna teks putih */
            font-size: 24px;
            font-weight: 500;
            margin: 0;
            margin-bottom: 16px;
        }
        .message {
            font-size: 15px;
            margin: 0;
            line-height: 1.5;
        }
        .error-code {
            color: #9aa0a6; /* Warna teks untuk kode error */
            font-size: 13px;
            margin-top: 4px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zM9.17 17.17c-.39.39-1.02.39-1.41 0-.39-.39-.39-1.02 0-1.41.39-.39 1.02-.39 1.41 0 .39.39.39 1.03 0 1.41zm5.66 0c-.39.39-1.02.39-1.41 0-.39-.39-.39-1.02 0-1.41.39-.39 1.02-.39 1.41 0 .39.39.39 1.03 0 1.41zM13 9.5V13c0 .55-.45 1-1 1s-1-.45-1-1V9.5c0-.55.45-1 1-1s1 .45 1 1zM13 7h-2V6h2v1z"/>
    </svg>

    <h1 class="title">Simulasi 503 Service Unavailable</h1>

    <p class="message">
        Server tidak dapat menangani permintaan karena lalu lintas yang sangat tinggi.
        <br>
        <span class="error-code">ERR_CONNECTION_TIMED_OUT</span>
    </p>

</body>
</html>