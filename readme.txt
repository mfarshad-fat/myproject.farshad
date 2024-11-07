src--------------------------------------------
|  	allocation---------------------------------
|   |   
|	|	adapters-------------------
|   |   |   __init__.py
|   |   |   orm--
|   |   |   repositories--
|   |   |   dtos--      ???
|   |	|   mappers.py  ???
|   |   |   notifications.py        !!!
|   |   |   redis_eventpublisher.py !!!
|   |   |   -----------------------
|   |   
|	|	domain---------------------
|   |	|   __init__.py
|   |   |   entities--
|   |   |   services--
|   |   |   commands.py
|   |   |   events.py
|   |   |   enums.py            ???
|   |   |   -----------------------
|   |   
|	|	entrypoint-----------------
|   |   |   __init__.py
|   |   |   ajax_views--        ???
|   |   |   dependencies--      ???
|   |   |   routes--            ???
|   |   |   views--             ???
|   |   |   query_params.py     ???
|   |   |
|   |   |   redis_eventconsumer.py !!!
|   |   |   main.py             !!!
|   |   |   -----------------------
|   |
|	|	service_layer--------------
|   |   |   __init__.py
|   |   |   command_handlers--  ???
|   |   |   event_handlers--    ???
|   |   |   helpers--           ???
|   |   |   serializers--       ???
|   |   |   access_checker.py   ???
|   |   |   
|   |   |   messagebus.py       !!!
|   |   |   unit_of_work.py     !!!
|   |   |   -----------------------
|   |   __init__.py
|   |   bootstrap.py !!!
|   |   config.py    !!!
|   |   views        !!!
|   |   -----------------------------------------
|   __init__.py
|   setup.py         !!!
|   ---------------------------------------------
-------------------------------------------------------