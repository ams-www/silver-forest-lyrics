<ul>
  {{ range .Site.RegularPages.ByTitle }}
    <li><a href="{{ .RelPermalink }}">{{ .Title }}</a></li>
  {{ end }}
</ul>
