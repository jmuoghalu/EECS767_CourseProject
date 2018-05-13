<?php

    $query = $_REQUEST['query'];
    $command = 'python /home/j286m692/EECS_767/EECS767_CourseProject/engine/test.py ' . $query;
    // $command = '.\web_driver.py 2>&1' . $query;
    //echo $command;
    $from_python = exec($command, $o, $r);
    $from_python = json_decode($from_python, TRUE);
    /*var_dump($from_python);
    echo "<br />";
    echo "<br />";
    var_dump($o);
    echo "<br />";
    echo "<br />";
    var_dump($r);
    echo "<br />";
    echo "<br />";*/

    echo '
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

            <title>Search Results</title>
        </head>
        <body>
        <div class="container">
            <h1>Top 10 Search Results<h1><br /><ol>';
            foreach ($from_python as $i => $result_i)
            {
                echo '
                <br />
                <li>
                    <div class="row h-10 align-items-center">
                        <div class="col-12" style="text-align: left">
                            <a href=' . $result_i["url"] . '>' . $result_i["name"] . '</a>
                            <h3><font color="green">' . $result_i['url'] . '</font></h3>
                            <h3>' . $result_i["snapshot"] . '<h/3>
                        </div>
                    </div>
                </li>
                <br />';
            }

        echo '
        </ol></div>


        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
        </body>
    </html>';
?>
