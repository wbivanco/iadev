# Skill: Smart Commit

## Propósito

Crear un commit local, atómico y trazable para una task revisada dentro del
flujo IADev.

## Entradas requeridas

- Task activa revisada y su evidencia.
- Aprobación humana explícita para crear el commit.
- Estado y diff actuales del repositorio.

## Procedimiento

1. Confirmar que la task activa fue aceptada en revisión y que existe la
   aprobación de commit correspondiente.
2. Revisar `git status`, el diff sin preparar y el diff preparado para
   identificar sólo los cambios de la task activa.
3. Si hay archivos ajenos, contenido sensible, conflictos o cambios no
   relacionados, no crear el commit: reportar el bloqueo y solicitar decisión.
4. Preparar únicamente las rutas explícitas asociadas a la task aprobada.
5. Validar el área preparada con `git diff --cached --check`.
6. Crear un único commit local con un título breve que describa el resultado
   de la task y un cuerpo que indique alcance, validación y riesgos si aplican.
7. Informar hash, título, archivos incluidos y estado final del repositorio
   como evidencia para Closeout.

## Límites

- No crear el commit sin aprobación humana explícita.
- No incluir cambios ajenos a la task, secretos, archivos temporales ni
  artefactos generados innecesarios.
- No hacer `push`, no reescribir historial, no usar `commit --amend`,
  `reset`, `rebase` ni comandos destructivos.
