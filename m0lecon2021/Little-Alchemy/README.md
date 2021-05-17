# Little-Alchemy - m0lecon Teaser 2021

- Category: pwn
- Points: 190
- Solves: 24
- Solved by: drw0if

## Description

Alchemy is a wonderful world to explore. Are you able to become a skilled scientist? We need your help to discover many mysterious elements!

`nc challs.m0lecon.it 2123`

Note: the flag is inside the binary, and clearly it is different on the remote server.

## Solution

We are given an ELF binary compiler from C++, reversing it we can build up all the classes used inside it:

### Element:

| Field | Type | Size |
|-------|------|------|
| v_table |pointer| 8 |
| type | byte | 1 |
| padding || 7 |
| id | long | 8 |
| value | char[] |16|

### ComposedElement:
| Field | Type | Size |
|-------|------|------|
| element | Element | 40 |
| pointer? | | 8 |
| pointer? | | 8 |
| first_suorce | Element* | 8 |
| second_source| Element* |8 |

### Handler:
| Field | Type | Size |
|-------|------|------|
| flag_element | Element | 40 |
| fire_element | Element | 40 |
| air_element | Element | 40 |
| earth_element | Element | 40 |
| elements | Element*[10] | 80 |
| element_handler | ElementHandler | ? |

So as we can guess `ComposedElement` is a subclass of `Element` class and some methods are virtual, so there is a virtual table somewhere.

Let's focus on the code logic:

```C++
int main()

{
  Handler handler_pointer;
  
  Handler::Handler(&handler_pointer);
  Handler::init(&handler_pointer);
  Handler::menu(&handler_pointer);
  Handler::~Handler(&handler_pointer);
  return 0;
}
```

The Handler constructor is a lot interesting: 
```C++
void __thiscall Handler::Handler(Handler *this)

{
  size_t flag_len;
  undefined *flag_ptr;
  
  Element::Element((Element *)this,1);
  Element::Element(&this->fire,2);
  Element::Element(&this->air,4);
  Element::Element(&this->earth,8);
  ElementHandler::ElementHandler(&this->handler);
  flag_ptr = flag;
  flag_len = strlen(flag);

  std::copy<char_const*,char*>(flag,flag_ptr + flag_len,(this->flag_element).value);
  return;
}
```
it creates 4 `Element` objects with the ids: 1, 2, 4, 8 and in the end it copies the flag string inside the value of the first one, these objects are stored inside the `Handler` object.

The `init` method just set each array entry inside the Handler object to NULL.
The real software logic is implemented inside the `menu` function. Inside we can found the banner print, the input parsing and all the actions we can perform.

### Create Element
Firing this option we are asked to insert the position we want to use for the new Element object and two ids of already existing elements which will be combined to build new elements, as an example we can say -1 (Water) and -2 (Fire) and we get Vapor! This is implemented inside the `combineElements` method:

```C++
ComposedElement * __thiscall
ElementHandler::combineElements(ElementHandler *this,Element *source_1,Element *source_2)

{
  char cVar1;
  ComposedElement *new_object;
  ulong new_object_id;
  basic_ostream *pbVar2;
  
  if ((source_1 == (Element *)0x0) || (source_2 == (Element *)0x0)) {
    new_object = (ComposedElement *)0x0;
  }
  else {
    new_object_id = source_2->id ^ source_1->id;
    cVar1 = isValidElement(this,new_object_id); // return new_object_id < 10;
    if (cVar1 == '\x01') {
      if ((new_object_id == 0) && (source_1->type != 0)) {
        new_object = (ComposedElement *)operator.new(0x28);
        Element::Element((Element *)new_object,(ElementType)source_1->id);
        pbVar2 = std::operator<<((basic_ostream *)std::cout,"[*] created ");
        pbVar2 = std::operator<<(pbVar2,(new_object->element_object).value);
        pbVar2 = std::operator<<(pbVar2,"!");
        std::basic_ostream<char,std::char_traits<char>>::operator<<
                  ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
                   std::endl<char,std::char_traits<char>>);
      }
      else {
        new_object = (ComposedElement *)operator.new(0x48);
        ComposedElement::ComposedElement(new_object,(ElementType)new_object_id);
        ComposedElement::setSources(new_object,source_1,source_2);
        pbVar2 = std::operator<<((basic_ostream *)std::cout,"[*] created ");
        pbVar2 = std::operator<<(pbVar2,(new_object->element_object).value);
        pbVar2 = std::operator<<(pbVar2,"!");
        std::basic_ostream<char,std::char_traits<char>>::operator<<
                  ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
                   std::endl<char,std::char_traits<char>>);
      }
    }
    else {
      pbVar2 = std::operator<<((basic_ostream *)std::cout,
                               "[-] not possible to combine this two elements!");
      std::basic_ostream<char,std::char_traits<char>>::operator<<
                ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
                 std::endl<char,std::char_traits<char>>);
      new_object = (ComposedElement *)0x0;
    }
  }
  return new_object;
}
```
so if the sources are of the same element and they are the basic type it builds a new `Element` object if the twi elements are different it build a `ComposedElement` object and set the sources:

```C++
void __thiscall ComposedElement::setSources(ComposedElement *this,Element *param_1,Element *param_2)

{
  this->first_source = param_1;
  this->second_source = param_2;
  return;
}
```

So if we build an element with the Water (-1) we get a composed element with a pointer to the water object whose string is the actual flag.

### Print Element and Print All
It asks us for an element and prints its value or it prints all the values of the existing elements in the array.

### Edit element
We are asked for the array element we want to edit the value of. The editing is made through the `cin` global object directly into the character array. This leads to a buffer overflow! With this flaw we can overwrite all the data on the heap starting from the string value of an object and keep going to the next element data. Unlucky it puts a `\0` at the end of the readed data so we can't leak any information.

```C++
void __thiscall Element::customizeName(Element *this)

{
  std::operator>>((basic_istream *)std::cin,this->value);
  return;
}
```

### Delete element
It asks us for the array element to delete, the element is deleted by calling the destructor, then the array pointer is set to NULL. No use-after-free available.

### Copy name
We can copy the string value from an element to another element:
```C++
undefined8 __thiscall
ElementHandler::copyName(ElementHandler *this,Element *param_1,Element *param_2)

{
  long lVar1;
  size_t sVar2;
  undefined8 ans;
  
  if ((param_1 == (Element *)0x0) || (param_2 == (Element *)0x0)) {
    ans = 0;
  }
  else {
    if (param_1->type == 0) {
      if (param_1 == (Element *)0x0) {
        lVar1 = 0;
      }
      else {
        lVar1 = __dynamic_cast(param_1,&Element::typeinfo,&ComposedElement::typeinfo,0);
      }
      sVar2 = strlen((char *)(lVar1 + 0x28));
      std::copy<char*,char*>((char *)(lVar1 + 0x18),(char *)(lVar1 + 0x28 + sVar2),param_2->value);
    }
    else {
      std::copy<char*,char*>(param_1->value,(char *)(param_1 + 1),param_2->value);
    }
    ans = 1;
  }
  return ans;
}
```

## Exploit
Using the `std::copy` function we can specify the starting point and the ending point, used in this way though the leading `\0` is not copied, so if we overwrite the string and then copy it from an element to another element we can leak information. Our working approach is in fact:
- Leak the vtable address with this combo overflow + copy
- Update the vtable pointer to something useful
- Trigger the programm to use the malicious vtable

We should first find something useful, luckily the `ComposedElement` class has a never called method `showSources`:
```C++
void __thiscall ComposedElement::showSources(ComposedElement *this)

{
  basic_ostream *pbVar1;
  
  pbVar1 = std::operator<<((basic_ostream *)std::cout,this->first_source->value);
  pbVar1 = std::operator<<(pbVar1," + ");
  pbVar1 = std::operator<<(pbVar1,this->second_source->value);
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  return;
}
```

Analyzing the vtable we can find that the `destructor` is 8 byte before the `showSources` so if we add 8 to the `~ComposedElement` address we can then use the delete option to fire the `showSources`. If we build an element made from water the source is the flag!

[Exploit](dist/exploit.py)

```
ptm{vT4bl3s_4r3_d4ng3r0us_019}
```