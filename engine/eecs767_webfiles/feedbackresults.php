<?php

    $relAndIrrel = "";
    $num_results = $_REQUEST["num_results"];
    $query = $_REQUEST["query"];

    $x = 0;
    $y = 1;
    while( $x < $num_results )
    {
        $y_val = "check_result_" . $y;
        $box_y = $_REQUEST[$y_val];
        if ( $box_y == strval($y) )
        {
            if ($y == 1)
            {
                echo "Checked a Box<br /><br";
                $relAndIrrel = $relAndIrrel . strval($y);
            }
            else
            {
                if($relAndIrrel != "")
                {
                    $relAndIrrel = $relAndIrrel . "_" . strval($y);
                }
                else
                {
                    $relAndIrrel = $relAndIrrel . strval($y);
                }
            }
        }
        $x += 1;
        $y += 1;
    }

    $command = 'cd ../../EECS_767/EECS767_CourseProject/source/ && python3 step6_web_results.py ' . $query . ' ' . $relAndIrrel;
    $from_python = exec($command, $o, $r);
    $from_python = json_decode($from_python, TRUE);

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
    <h1>Here Are the Updated Search Results for Relevance Feedback<h1><br /><ol>';

    $num_results = 0;
    foreach ($from_python as $i => $result_i)
    {
        $result_i["url"] = str_replace("%3A", ":", $result_i["url"]);
        $result_i["url"] = str_replace("%2F", "/", $result_i["url"]);
        $result_i["url"] = str_replace("%2E", ".", $result_i["url"]);
        $result_i["url"] = str_replace(".html", "", $result_i["url"]);
        $result_i["url"] = str_replace(".htm", "", $result_i["url"]);
        echo '
        <br />
        <li>
        <div class="row h-10 align-items-center">
            <div class="col-12" style="text-align: left">
            <a href=' . $result_i["url"] . '>' . $result_i["url"] . '</a>
            <h3><font color="green">' . $result_i['url'] . '</font></h3>
            <h3><font color="black">' . $result_i['snapshot'] . '</font></h3>
            </div>
        </div>
        </li>
        <br />';
        $num_results += 1;
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
