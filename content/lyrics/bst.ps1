$target = "y1zƒ{[ƒJƒ‹‹È‰ÌŒˆê——‚Ö"

Get-ChildItem -Filter *.md | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $new = $content -replace "(?s)$target.*", ""
    Set-Content $_.FullName $new -Encoding UTF8
}
