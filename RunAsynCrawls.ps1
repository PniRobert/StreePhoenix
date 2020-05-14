For ($i = 0; $i -le 50; $i++) {
    Start-Process python .\AsyncCrawl.py -RedirectStandardOutput "output_$($i).log" -RedirectStandardError "error_$($i).log"
}