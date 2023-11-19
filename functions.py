class ListNode:
    def __init__(self, val=0, next=None, prev=None):
             self.val = val
             self.next = next
             self.prev = prev

def create_circular_linked_list(a,b,c,d):
    a = ListNode(a)
    b = ListNode(b)
    c = ListNode(c)
    d = ListNode(d)
    a.next = b
    b.next = c
    c.next = d
    d.next = a
    a.prev = d
    d.prev = c
    c.prev = b
    b.prev = a
    return [a,b,c,d]

def draw_text(surface, text,font,text_color,x,y):
    img=font.render(text,True,text_color)
    surface.blit(img,(x,y))





