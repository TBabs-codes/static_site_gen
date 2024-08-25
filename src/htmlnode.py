
#Tag types


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("somebody has work todo")
    
    def props_to_html(self):
        key_val_string = ""
        for key, value in self.props.items():
            key_val_string+= f" {key}=\"{value}\""

        return key_val_string

    def __repr__(self):
        return f"HTMLNode():\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf has not value.")
        
        if self.tag == None:
            return self.value
        
        match self.tag:
            
            case 'p': #paragraph
                return f"<p>{self.value}</p>" 
            case 'a': #link
                return f"<a href=\"{self.props['href']}\">{self.value}</a>"
            case 'h': #header
                return f"<h1>{self.value}</h1>"
            case 'b': 
                return f"<b>{self.value}</b>"
            case 'i': 
                return f"<i>{self.value}</i>"
            case 'code':
                return f"<code>{self.value}</code>"
            case _: #raw_text
                return self.value
            

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Value Error1: ParentNode tag is None.")
        if self.children == None:
            raise ValueError("Value Error2: No children found in ParentNode.")
        elif len(self.children) == 0:
            raise ValueError("Value Error3: No children found in ParentNode.")

        
        html_string = ""

        for child in self.children:
            if isinstance(child, LeafNode):
                html_string += child.to_html()
            elif isinstance(child, ParentNode):
                html_string += child.to_html()
            else:
                raise TypeError("There is a item in children that is not a Parent or Leaf.")
            
        return f"<{self.tag}>{html_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"