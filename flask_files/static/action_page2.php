<html>
<body>

Your cURL was: <?php echo "curl -X GET --header 'Accept: application/json' https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?size=" . $_GET["size"] . "&official_title_fulltext=" . $_GET["query"] . "&include=official_title&include=nct_id&include=diseases&include=eligibility"  ?><br>

</body>
</html>
