Описание формата конфига:

**Параметры парсеров**
Параметры парсеров находятся в parsers. Там перечислены все имеющиеся парсеры. Для каждого парсера есть набор полей, описывающих их поведение:
[limit] ограничение по количеству объектов на странице
[max_offset] парсер не будет устанавливать значения offset большим чем значение в этом поле
[filename] название файла, в который парсер будет выгружать данные
[features] фичи, которые появятся в файле (желательно оставить как есть и не конфигурировать, но можно убрать ненужные) # возможно потом тут потребуется немного другая логика
[get_iterate] иногда перед получением всех ссылок для парсинга нам надо поперебирать несколько вариантов фильтров, так как к примеру домклик 
В этом словаре надо выписать все параметры фильтрации и их значения в массив 
пример:
{
    "city" : [1, 2, 3]
    "color": ["red", "green"]
    "type" : ...
}
Обязательно надо указать поле [type], оно может принимать 2 значения: [pairwise] и [linear].
[pairwise] - значения будут перебираться в соответствии с декартовым произведением (каждый с каждым) 
[linear] - значения будут перебираться линейно (1 элемент из всех массивов, затем 2 из всех и т.д.). В данном случае длины массивов должны быть одинаковы
Чтобы парсить ссылки без фильтров следует оставить поле [get_iterate] пустым (`get_iterate: {}`) 