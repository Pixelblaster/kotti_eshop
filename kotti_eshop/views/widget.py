from deform.widget import SelectWidget


class SelectizeWidget(SelectWidget):

    template = "kotti_eshop:templates/widget/selectize.pt"
    multiple = True
    css_class = 'selectize'

