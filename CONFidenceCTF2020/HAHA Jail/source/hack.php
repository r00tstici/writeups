<?hh

<<__EntryPoint>>
function main(): void {
    include_once(__DIR__.'/../vendor/autoload.hack');
     \Facebook\AutoloadMap\initialize();
    if(isset($_REQUEST['cmd'])){
        if($_REQUEST['cmd'] != ''){
            $uuid_generator = new \Usox\HackUuidGen\UuidGenerator();
            $uuid = $uuid_generator->generate();
            if (preg_match('/(([)]|["]|[\']|pcntl_alarm|pcntl_fork|pcntl_waitpid|file|pcntl_wait|pcntl_wifexited|pcntl_wifstopped|pcntl_wifsignaled|scandir|pcntl_wexitstatus|pcntl_wtermsig|pcntl_wstopsig|pcntl_signal|pcntl_signal_dispatch|pcntl_get_last_error|pcntl_strerror|pcntl_sigprocmask|pcntl_sigwaitinfo|pcntl_sigtimedwait|pcntl_exec|pcntl_getpriority|pcntl_setpriority|exec|shell_exec|proc_open|popen|system|passthru|file_get_contents|readfile|fopen|ini_set|fgets|fgetcsv|parse_ini_file|rename|copy|symlink|fseek|file_exists|delete|chmod|fpassthru|freed|fscanf|stream_wrapper_register|stream_wrapper_restore|fsockopen|pfsockopen|curl_init|stream_context_create|show_source|highlight_file|sleep|token_get_all|yaml_parse_file)(\s+)?\()|\$|\/\*.*\*\/|\/\/|\.|\//i', $_REQUEST['cmd'])){
                echo 'Leave me alone hacker'; die();
            }
            // run the code in hhvm (ignore nsjail, it's only to make this RCE more secure)
            $file = fopen('../'.$uuid.".php",'w');
            fwrite($file,$_REQUEST['cmd']);
            fclose($file);
            shell_exec("/usr/bin/cgcreate -g memory,pids,cpu:NSJAIL");
            if ($x = shell_exec('/bin/nsjail --cgroup_cpu_ms_per_sec 500 --cgroup_pids_max 16  --time_limit 5 --user 1000:1000 --group 1000:1000 -q -B /var -R /bin -R /usr -R /lib -R /lib64 -R /etc -R /opt -B /dev/urandom -B /home /usr/bin/hhvm /var/www/'.$uuid.'.php 2> /dev/stdout 1> /dev/null')) echo $x;
            else echo "$uuid.php written";
            unlink("../$uuid.php");
        }
        else echo "<div style='margin: 0 auto;text-align: center'><img src='prison.png'><h2>What am I doing hereeee?</h2></div>";    
    }
else echo "<div style='margin: 0 auto;text-align: center'><img src='prison.png'><h2>What am I doing hereeee?</h2></div>";    
}

