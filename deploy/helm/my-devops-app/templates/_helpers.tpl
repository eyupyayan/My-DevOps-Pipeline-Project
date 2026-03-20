{{- define "my-devops-app.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "my-devops-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}