# IADev

Kit de coordinación para desarrollar con Cursor, Codex o Claude Code. El motor se instala una vez por máquina. Cada producto guarda solo su memoria en `ai-system/` y su código en la raíz del propio repo.

## Instalar el motor, una vez por máquina

```bash
git clone <url-de-este-repo> ~/herramientas/iadev
~/herramientas/iadev/install.sh
```

`install.sh` enlaza los skills a `~/.agents/skills/` y a `~/.claude/skills/`, y los agentes de Codex a `~/.codex/agents/`. No copia nada dentro de los productos y no recorre tus repos. Cursor y Codex leen `~/.agents/skills/`. Claude Code lee `~/.claude/skills/`. Los archivos `.toml` los usa Codex; Cursor no los necesita.

## Inicializar cada producto

El script queda en el kit. No lo copies. Parado en la raíz del producto:

```bash
cd ~/proyectos/clinica
git init
~/herramientas/iadev/init.sh
```

`init.sh` crea, si no existen:

- `AGENTS.md`, corto, para que el chat arranque como coordinador
- `ai-system/`, con brief, perfil, backlog y estado en borrador
- las exclusiones `ai-system` y `AGENTS.md` en `.dockerignore`

Si un archivo ya existe, lo deja. El perfil queda con `code_root: .`: el código es la raíz de ese repo.

Después se abre el proyecto en el editor y se escribe la idea. El coordinador sigue el skill `aidev-coordinator` y completa `ai-system/` conversando. Esos archivos se commitean. El motor no.

En otra máquina: clonar el kit, correr `install.sh`, clonar el producto. `AGENTS.md` y `ai-system/` ya vienen en ese clone.

## Actualizar

En el kit:

```bash
git pull
```

Un cambio en un skill o agente que ya estaba enlazado se ve en todos los proyectos. Una carpeta nueva no tiene enlace hasta correr `install.sh` otra vez en esa máquina.

## Despliegue

`ai-system/` y `AGENTS.md` viajan en git y no deben publicarse.

- Docker: `init` los agrega a `.dockerignore`.
- Si el pipeline publica solo `dist/`, `build/` o un binario, no entran al artefacto.
- Si el servidor hace `git pull` del repo completo, excluí `ai-system/` y `AGENTS.md` en esa herramienta (por ejemplo `.vercelignore` o `rsync --exclude`). `.dockerignore` en ese caso no actúa.

## Skill de un solo producto

Va en ese repo, en `.agents/skills/nombre/SKILL.md`, y se commitea ahí. Convive con los skills del home. `install.sh` no lo pisa.

El detalle del ciclo de trabajo está en [ai-system/docs/adoption-guide.md](ai-system/docs/adoption-guide.md).
