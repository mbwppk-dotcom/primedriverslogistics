# Replace Logo Script for Prime Drivers Website
# Updates both the Header (logo.png) and Footer (logo-white.png) across all HTML pages.

$projectRoot = "D:\prime-drivers-website"
$headerLogo = "images/logo.png"
$footerLogo = "images/logo-white.png"

$headerLogoHtml = @"
    <a href="index.html" class="logo" aria-label="Prime Drivers Logistics home">
      <img src="${headerLogo}" alt="Prime Drivers Logistics" class="logo-img" />
    </a>
"@

$footerLogoHtml = @"
        <a href="index.html" class="logo" aria-label="Prime Drivers Logistics home">
          <img src="${footerLogo}" alt="Prime Drivers Logistics" class="logo-img footer-logo" />
        </a>
"@

$patternHeader = '(?s)<a href="index\.html" class="logo" aria-label="Prime Drivers Logistics home">.*?</a>'
$patternFooter = '(?s)<a href="index\.html" class="logo"(?: aria-label="Prime Drivers Logistics home")?>\s*<img[^>]*footer-logo[^>]*>\s*</a>|<a href="index\.html" class="logo">.*?</a>'

Get-ChildItem -Path $projectRoot -Filter *.html | ForEach-Object {
    $filePath = $_.FullName
    $content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    
    $content = [regex]::Replace($content, $patternHeader, $headerLogoHtml, 1)
    $content = [regex]::Replace($content, $patternFooter, $footerLogoHtml, 1)
    [System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
    Write-Host "Updated $($_.Name)"
}

Write-Host "Logo update complete."
