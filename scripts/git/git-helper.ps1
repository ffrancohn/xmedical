#Requires -Version 5.1
<#
.SYNOPSIS
    Asistente Git interactivo para Windows (portable entre repositorios).

.DESCRIPTION
    Copia la carpeta scripts/git/ a cualquier sitio y ejecuta git-helper.cmd
    desde la raíz de un repositorio, o pasa la ruta como argumento.

.EXAMPLE
    .\git-helper.cmd
    .\git-helper.cmd C:\ruta\a\mi-repo
#>
param(
    [Parameter(Position = 0)]
    [string]$RepoPath = "",
    [ValidateSet("", "status", "diff", "commit", "fetch", "pull", "push", "sync", "log", "branch", "stash", "help")]
    [string]$Action = ""
)

$ErrorActionPreference = "Stop"

function Write-Title([string]$Text) {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Explain([string]$Text) {
    Write-Host "  * $Text" -ForegroundColor DarkGray
}

function Write-Ok([string]$Text) {
    Write-Host "  + $Text" -ForegroundColor Green
}

function Write-Warn([string]$Text) {
    Write-Host "  ! $Text" -ForegroundColor Yellow
}

function Write-Err([string]$Text) {
    Write-Host "  X $Text" -ForegroundColor Red
}

function Ensure-GitRepo {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Err "La ruta no existe: $Path"
        exit 1
    }
    Set-Location -LiteralPath $Path
    $root = git rev-parse --show-toplevel 2>$null
    if (-not $root) {
        Write-Err "No es un repositorio Git: $Path"
        Write-Explain "Inicializa uno con: git init"
        exit 1
    }
    Set-Location -LiteralPath $root
    return $root
}

function Invoke-Git {
    param([string[]]$Args)
    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') falló (código $LASTEXITCODE)"
    }
}

function Read-YesNo {
    param(
        [string]$Prompt,
        [bool]$Default = $true
    )
    $hint = if ($Default) { "S/n" } else { "s/N" }
    $answer = Read-Host "$Prompt [$hint]"
    if ([string]::IsNullOrWhiteSpace($answer)) { return $Default }
    return $answer -match '^[sSyY]'
}

function Pause-Continue {
    Write-Host ""
    Read-Host "Pulsa Enter para volver al menú" | Out-Null
}

function Show-RepoInfo {
    $branch = git branch --show-current 2>$null
    if (-not $branch) { $branch = "(sin rama)" }
    $remote = git remote get-url origin 2>$null
    if (-not $remote) { $remote = "(sin remoto origin)" }
    Write-Host "  Repositorio: $(Get-Location)" -ForegroundColor White
    Write-Host "  Rama:        $branch" -ForegroundColor White
    Write-Host "  Remoto:      $remote" -ForegroundColor White
}

function Action-Status {
    Write-Title "Estado del repositorio (git status)"
    Write-Explain "Muestra qué archivos cambiaron, cuáles están listos para commit"
    Write-Explain "y si tu rama va adelantada o atrasada respecto al remoto."
    Write-Host ""
    Invoke-Git status
}

function Action-Diff {
    Write-Title "Cambios sin preparar (git diff)"
    Write-Explain "Compara tu copia de trabajo con el último commit."
    Write-Explain "Útil antes de hacer commit para revisar qué modificaste."
    Write-Host ""
    Invoke-Git diff
    if (Read-YesNo "¿Ver también cambios ya preparados (staged)?" $false) {
        Write-Host ""
        Invoke-Git diff --staged
    }
}

function Action-Commit {
    Write-Title "Crear commit"
    Write-Explain "Un commit guarda una instantánea de los cambios con un mensaje."
    Write-Explain "Primero se preparan archivos (git add); luego se confirma (git commit)."
    Write-Host ""
    Invoke-Git status -sb
    Write-Host ""

    $mode = Read-Host "¿Qué preparar? [1] Todo  [2] Solo archivos que elijas  [3] Cancelar"
    switch ($mode) {
        "1" {
            Write-Explain "git add -A: incluye archivos nuevos, modificados y borrados."
            if (-not (Read-YesNo "¿Preparar todos los cambios?" $true)) { return }
            Invoke-Git add -A
        }
        "2" {
            Write-Explain "Escribe rutas separadas por espacio (ej: src/app.py docs/readme.md)"
            $paths = Read-Host "Archivos o carpetas"
            if ([string]::IsNullOrWhiteSpace($paths)) {
                Write-Warn "Cancelado: no indicaste archivos."
                return
            }
            Invoke-Git add -- $paths.Split(" ", [StringSplitOptions]::RemoveEmptyEntries)
        }
        default {
            Write-Warn "Cancelado."
            return
        }
    }

    Write-Host ""
    Write-Explain "Cambios que entrarán en el commit:"
    Invoke-Git diff --staged --stat
    Write-Host ""

    $hasStaged = git diff --staged --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Warn "No hay cambios preparados. Nada que commitear."
        return
    }

    do {
        $message = Read-Host "Descripción del commit (obligatoria)"
    } while ([string]::IsNullOrWhiteSpace($message))

    if (-not (Read-YesNo "¿Crear commit con ese mensaje?" $true)) {
        Write-Warn "Commit cancelado. Los archivos siguen preparados (staged)."
        return
    }

    Invoke-Git commit -m $message
    Write-Ok "Commit creado."
    Write-Host ""
    Invoke-Git log -1 --oneline
}

function Action-Fetch {
    Write-Title "Descargar del remoto (git fetch)"
    Write-Explain "Descarga commits y ramas del servidor SIN mezclarlos en tu copia."
    Write-Explain "Sirve para ver si hay novedades antes de hacer pull o push."
    Write-Explain "Tu código local no cambia; solo se actualiza la información del remoto."
    Write-Host ""
    $remote = Read-Host "Remoto [origin]"
    if ([string]::IsNullOrWhiteSpace($remote)) { $remote = "origin" }
    Invoke-Git fetch $remote --prune
    Write-Ok "Fetch completado."
    Write-Host ""
    Write-Explain "Resumen respecto al remoto:"
    Invoke-Git status -sb
}

function Action-Pull {
    Write-Title "Traer y fusionar (git pull)"
    Write-Explain "Equivale a: fetch + integrar cambios del remoto en tu rama actual."
    Write-Explain "Úsalo cuando quieras actualizar tu copia con lo que hay en GitHub/GitLab."
    Write-Explain "Si hay conflictos, Git te pedirá resolverlos en los archivos marcados."
    Write-Host ""
    $branch = git branch --show-current
    Write-Host "  Rama actual: $branch" -ForegroundColor White
    Write-Host ""
    if (-not (Read-YesNo "¿Ejecutar git pull?" $true)) { return }
    Invoke-Git pull
    Write-Ok "Pull completado."
}

function Action-Push {
    Write-Title "Subir al remoto (git push)"
    Write-Explain "Envía tus commits locales al servidor (GitHub, GitLab, etc.)."
    Write-Explain "Solo sube lo que ya commiteaste; los cambios sin commit no viajan."
    Write-Host ""
    $branch = git branch --show-current
    if (-not $branch) {
        Write-Err "No hay rama activa."
        return
    }
    Invoke-Git status -sb
    Write-Host ""
    $upstream = git rev-parse --abbrev-ref "@{u}" 2>$null
    if (-not $upstream) {
        Write-Warn "La rama '$branch' no tiene remoto configurado."
        Write-Explain "La primera vez suele usarse: git push -u origin $branch"
        if (Read-YesNo "¿Configurar y subir a origin/$branch?" $true) {
            Invoke-Git push -u origin $branch
            Write-Ok "Push completado y rama enlazada con origin/$branch."
        }
        return
    }
    if (-not (Read-YesNo "¿Subir commits a $upstream?" $true)) { return }
    Invoke-Git push
    Write-Ok "Push completado."
}

function Action-Sync {
    Write-Title "Sincronizar (fetch + estado + pull opcional)"
    Write-Explain "Flujo recomendado antes de trabajar o antes de push:"
    Write-Explain "  1) fetch - ver que hay en el remoto"
    Write-Explain "  2) status - ver si vas adelantado/atrasado"
    Write-Explain "  3) pull - traer cambios si hace falta"
    Write-Host ""
    Invoke-Git fetch origin --prune
    Write-Ok "Fetch hecho."
    Write-Host ""
    Invoke-Git status -sb
    Write-Host ""
    $behind = git rev-list --count "HEAD..@{u}" 2>$null
    if ($LASTEXITCODE -eq 0 -and [int]$behind -gt 0) {
        Write-Warn "Tu rama está $behind commit(s) detrás del remoto."
        if (Read-YesNo "¿Hacer pull ahora?" $true) {
            Invoke-Git pull
            Write-Ok "Pull completado."
        }
    } else {
        Write-Ok "No necesitas pull (o no hay remoto enlazado)."
    }
}

function Action-Log {
    Write-Title "Historial reciente (git log)"
    Write-Explain "Lista los últimos commits: hash corto, autor, fecha y mensaje."
    Write-Host ""
    $n = Read-Host "¿Cuántos commits mostrar? [10]"
    if ([string]::IsNullOrWhiteSpace($n)) { $n = 10 }
    Invoke-Git log -n ([int]$n) --oneline --graph --decorate
}

function Action-Branch {
    Write-Title "Ramas"
    Write-Explain "Una rama es una línea de trabajo. 'main' suele ser la principal."
    Write-Host ""
    Invoke-Git branch -vv
    Write-Host ""
    $choice = Read-Host "¿Crear rama nueva? [s/N]"
    if ($choice -match '^[sSyY]') {
        $name = Read-Host "Nombre de la rama"
        if (-not [string]::IsNullOrWhiteSpace($name)) {
            Invoke-Git checkout -b $name
            Write-Ok "Rama '$name' creada y activa."
        }
    }
}

function Action-Stash {
    Write-Title "Guardar cambios temporalmente (git stash)"
    Write-Explain "Oculta cambios sin commitear para cambiar de rama o hacer pull limpio."
    Write-Explain "Recuperas después con: git stash pop"
    Write-Host ""
    Write-Host "  [1] Guardar cambios (stash)"
    Write-Host "  [2] Ver lista de stashes"
    Write-Host "  [3] Recuperar el último (stash pop)"
    Write-Host "  [0] Volver"
    $c = Read-Host "Opción"
    switch ($c) {
        "1" {
            $msg = Read-Host "Nota opcional"
            if ([string]::IsNullOrWhiteSpace($msg)) { Invoke-Git stash push -u }
            else { Invoke-Git stash push -u -m $msg }
            Write-Ok "Cambios guardados en stash."
        }
        "2" { Invoke-Git stash list }
        "3" {
            if (Read-YesNo "¿Aplicar y quitar el último stash?" $true) {
                Invoke-Git stash pop
            }
        }
    }
}

function Show-Help {
    Write-Title "Cuándo usar cada comando"
    @"
  git status   -> Siempre antes de commit/push. Que cambio? Que falta subir?
  git diff     -> Revisar el detalle de cambios antes de commitear.
  git commit   -> Guardar una version local con descripcion.
  git fetch    -> Ver novedades del servidor SIN modificar tus archivos.
  git pull     -> Traer cambios del remoto e integrarlos en tu rama.
  git push     -> Subir tus commits al servidor.
  git log      -> Ver historial de commits.
  git stash    -> Apartar cambios a medias sin perderlos.

  Flujo tipico del dia:
    1) Sync (fetch + pull si hace falta)
    2) Trabajar y guardar archivos
    3) Status + Diff
    4) Commit
    5) Push

  fetch vs pull:
    - fetch = solo descarga informacion
    - pull  = descarga Y fusiona en tu copia actual
"@ | Write-Host -ForegroundColor DarkGray
}

function Show-Menu {
    Write-Host ""
    Write-Host "  Git Helper - menu principal" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1]  Estado (status)"
    Write-Host "  [2]  Ver cambios (diff)"
    Write-Host "  [3]  Commit (te pide descripción)"
    Write-Host "  [4]  Fetch (descargar sin fusionar)"
    Write-Host "  [5]  Pull (traer y fusionar)"
    Write-Host "  [6]  Push (subir commits)"
    Write-Host "  [7]  Sync (fetch + pull si hace falta)"
    Write-Host "  [8]  Historial (log)"
    Write-Host "  [9]  Ramas"
    Write-Host "  [10] Stash (guardar cambios temporalmente)"
    Write-Host "  [h]  Ayuda: cuándo usar cada comando"
    Write-Host "  [0]  Salir"
    Write-Host ""
}

# --- Inicio ---
if (-not [string]::IsNullOrWhiteSpace($RepoPath)) {
    $repoRoot = Ensure-GitRepo -Path (Resolve-Path -LiteralPath $RepoPath).Path
} else {
    $repoRoot = Ensure-GitRepo -Path (Get-Location).Path
}

Write-Title "Git Helper"
Show-RepoInfo

$runOnce = {
    param([scriptblock]$Block)
    try { & $Block } catch { Write-Err $_.Exception.Message }
    if ($Action) { return }
    Pause-Continue
}

if ($Action) {
    switch ($Action) {
        "status"  { & $runOnce { Action-Status }; exit 0 }
        "diff"    { & $runOnce { Action-Diff }; exit 0 }
        "commit"  { & $runOnce { Action-Commit }; exit 0 }
        "fetch"   { & $runOnce { Action-Fetch }; exit 0 }
        "pull"    { & $runOnce { Action-Pull }; exit 0 }
        "push"    { & $runOnce { Action-Push }; exit 0 }
        "sync"    { & $runOnce { Action-Sync }; exit 0 }
        "log"     { & $runOnce { Action-Log }; exit 0 }
        "branch"  { & $runOnce { Action-Branch }; exit 0 }
        "stash"   { & $runOnce { Action-Stash }; exit 0 }
        "help"    { Show-Help; exit 0 }
    }
}

while ($true) {
    Show-Menu
    $opt = Read-Host "Elige una opción"
    try {
        switch ($opt) {
            "1" { Action-Status }
            "2" { Action-Diff }
            "3" { Action-Commit }
            "4" { Action-Fetch }
            "5" { Action-Pull }
            "6" { Action-Push }
            "7" { Action-Sync }
            "8" { Action-Log }
            "9" { Action-Branch }
            "10" { Action-Stash }
            { $_ -in "h", "H", "?" } { Show-Help }
            "0" { Write-Ok "Hasta luego."; break }
            default { Write-Warn "Opción no válida." }
        }
    } catch {
        Write-Err $_.Exception.Message
    }
    if ($opt -ne "0") { Pause-Continue }
}
