#!/usr/bin/php
<?php

require_once('/usr/local/lib/php/common.php');
require_once('/usr/local/lib/php/os.php');


function get_history($from_id)
{
    printf("get_history %d\n", $from_id);
    file_put_contents('last_id.txt', $from_id);

    $data = array('symbol' => 'ETHUSDT', 'fromId' => $from_id);
    $url = 'https://api.binance.com/api/v1/historicalTrades?' . http_build_query($data);

    // use key 'http' even if you send the request to https://...
    $options = array(
        'http' => array(
            'header'  => "" .
                         "X-MBX-APIKEY: EJwG2th6QsQ0e6PPFeMzandmXbpZNhUGW6rxo7n81Ae4rDgVNC6SPJTkLCN83ZO1\r\n",
            'method'  => 'GET',
            'ignore_errors' => true,
        )
    );
    $context  = stream_context_create($options);
    $res = file_get_contents($url, false, $context);
    $data = json_decode($res, true);
    ksort($data, SORT_NUMERIC);
    return $data;
}


function main()
{
    //$start_id = 9097165;  // GMT: Sunday, February 4, 2018 5:07:23.014 PM
    @$start_id = (int)file_get_contents('last_id.txt');
    if (!$start_id)
        $start_id = 25177074 - 12*24*60*60;

    $finish_id = 25177074 - 8*24*60*60;
    printf("start_id = %d\n", $start_id);
    printf("finish_id = %d\n", $finish_id);

    $id = $start_id;
    $cnt = 0;
    for(;;) {
        if ($id > $finish_id) {
            printf("finished\n");
            break;
        }
        $part = get_history($id + 1);
        $first = false;

        if (!count($part))
            break;

        $price_text = "";
        foreach ($part as $point) {
            if ($point['id'] > $id)
                $id = $point['id'];

            if ($cnt > 200) {
                printf("time = %s\n", date('d.m.Y h:i:m', $point['time'] / 1000));
                $cnt = 0;
            }
            $cnt ++;
            $price_text .= sprintf("%d,%.2f\n", $point['time'], round($point['price'], 2));
        }
        file_put_contents('history.txt', $price_text, FILE_APPEND);
    }

    return 0;
}

return main();
