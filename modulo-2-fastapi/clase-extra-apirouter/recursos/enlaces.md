# Recursos: APIRouter y Organizacion de Proyecto

## Documentacion Oficial de FastAPI

- [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
  Tutorial oficial de FastAPI sobre como organizar proyectos grandes con APIRouter. Cubre la estructura de directorios, la creacion de routers en archivos separados y como montarlos en la app principal.

- [APIRouter class reference](https://fastapi.tiangolo.com/reference/apirouter/)
  Referencia completa de todos los parametros del constructor de APIRouter: prefix, tags, dependencies, responses, etc.

- [Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)
  Como usar dependencias a nivel de decorador y a nivel de router con el parametro `dependencies`.

- [Include Router](https://fastapi.tiangolo.com/reference/fastapi/#fastapi.FastAPI.include_router)
  Referencia de `app.include_router()` con todos sus parametros: router, prefix, tags, dependencies, responses.

## Starlette (framework base)

- [Starlette Routing](https://www.starlette.io/routing/)
  FastAPI esta construido sobre Starlette. El sistema de routing de Starlette es la base de APIRouter. Util para entender como funciona internamente.

## Articulos y Guias

- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
  Repositorio con patrones recomendados para proyectos FastAPI, incluyendo estructura de proyecto y organizacion de routers.
