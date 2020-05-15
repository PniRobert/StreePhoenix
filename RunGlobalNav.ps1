For ($i = 0; $i -le 20; $i++) {
    Start-Process python .\GlobalNav.py -RedirectStandardOutput "output_$($i).log" -RedirectStandardError "error_$($i).log"
}