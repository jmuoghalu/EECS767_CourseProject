<!doctype html>
<html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">

        <!-- Custom CSS -->
        <link href="searchstyle.css" rel="stylesheet">

        <title>EECS 767: Group 2's Search Engine</title>
    </head>
    <body>
        <div class="jumbotron h-100">
            <div class="row h-100 align-items-center">
                <div class="col-2"><br></div>
                <div class="col-8 align-self-center" style="text-align: center">
                    <h1>Welcome to the Search Engine</h1>
                    <br>

                    <form action="query.php">
                    <div class="input-group">
                        <input type="text" name="query" class="form-control" placeholder="Enter search query">
                    </div>
                    <div class="button-group">
                        <button type="submit" name="button" class="btn btn-default" value="BS">Basic Search</button>
                        <button type="submit" name="button" class="btn btn-default" value="TPS">Term Proximity Search</button>
                        <button type="submit" name="button" class="btn btn-default" value="RFS">Relevance Feedback Search</button>
                    </div>
                    </form>
                </div>
                <div class="col-2"><br></div>
            </div>
        </div>

        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
    </body>
</html>
