from .models import Entry, Project

def find_between( s, first, last ):
    try:
        start = s.index( first )
        end = s.index( last, start )+ len(last)
        return s[start:end]
    except ValueError:
        return ""


def create_project_tree(project_pk):
    project_tree_text="<R"+str(project_pk)+">\n<size>0</size>\n<name></name>\n<desc></desc>\n</R"+str(project_pk)+'>'

    return project_tree_text

def get_entry_type_based_on_parent(parent):
    parent_type=str(parent.entry_type)
    if parent_type == 'R':
        this_entry_type='C'
    elif parent_type=='C':
        this_entry_type='D'
    elif parent_type=='D':
        this_entry_type='V'
    return this_entry_type

def generate_tree_SVG(project):
    return tree_SVG

def add_requirement_to_tree(parent_pk):
    parent = Entry.objects.get(pk=parent_pk)
    project=parent.project
    parent_req_size=parent.number_of_sub_requirements
    file_text=project.project_tree
    parent_entry_id=parent.entry_id
    file_text_new=""
    new_entry_number=str(parent_req_size+1)
    type_letter="R"
    insert_type="requirements"
    new_entry_id=parent_entry_id+"\\"+type_letter+new_entry_number


    new_entry_pos=file_text.find("</requirements-"+parent_entry_id+">")
    file_text_new=file_text[:new_entry_pos]+"<"+new_entry_id+">\n<size>0</size>\n<name></name>\n<desc></desc>\n</"+new_entry_id+">\n"+file_text[new_entry_pos:]

    size_text=find_between(file_text_new,"<"+parent_entry_id+">","</r-size>")

    file_text_new=file_text_new.replace(size_text,size_text.replace("<r-size>"+str(parent_req_size)+"</r-size>","<r-size>"+new_entry_number+"</r-size>"))

    replace_project_tree(project, file_text_new)

    return new_entry_id


def add_entry_to_tree(parent_pk):
    parent=Entry.objects.get(pk=parent_pk)
    project=parent.project
    parent_entry_size=parent.number_of_children_entries
    parent_entry_id=parent.entry_id
    file_text=project.project_tree
    file_text_new=""
    new_entry_number=str(parent_entry_size+1)
    type_letter=get_entry_type_based_on_parent(parent)
    insert_type=""
    new_entry_id=parent_entry_id+"\\"+type_letter+new_entry_number


    if type_letter=="D":
        insert_type="designs"
        if parent_entry_size>0:
            new_entry_pos=file_text.find("</designs>\n<requirements-"+parent_entry_id+">")
            file_text_new=file_text[:new_entry_pos]+"<"+new_entry_id+">\n<size>0</size>\n<name></name>\n<desc></desc>\n</"+new_entry_id+">\n"+file_text[new_entry_pos:]
        elif parent_entry_size==0:
            new_entry_pos=file_text.find("<requirements-"+parent_entry_id+">")
            file_text_new=file_text[:new_entry_pos]+"<"+insert_type+">\n<"+new_entry_id+">\n<size>0</size>\n<name></name>\n<desc></desc>\n</"+new_entry_id+">\n</"+insert_type+">\n"+file_text[new_entry_pos:]

    elif type_letter=="V":
        insert_type="validations"
        if parent_entry_size>0:
            new_entry_pos=file_text.find("</"+parent_entry_id+"\\"+type_letter+str(parent_entry_size)+">\n")+len("</"+parent_entry_id+"\\"+type_letter+str(parent_entry_size)+">\n")
            file_text_new=file_text[:new_entry_pos]+"<"+new_entry_id+">\n<size>0</size>\n<name></name>\n<desc></desc>\n</"+new_entry_id+">\n"+file_text[new_entry_pos:]
        elif parent_entry_size==0:
            new_entry_pos=file_text.find("</"+parent_entry_id+">")
            file_text_new=file_text[:new_entry_pos]+"<"+insert_type+">\n<"+new_entry_id+">\n<size>0</size>\n<name></name>\n<desc></desc>\n</"+new_entry_id+">\n</"+insert_type+">\n"+file_text[new_entry_pos:]

    elif type_letter=="C":
        insert_type="concepts"
        if parent_entry_size>0:
            new_entry_pos=file_text.find("</concepts>\n</"+parent_entry_id+">")
            file_text_new=file_text[:new_entry_pos]+"<"+new_entry_id+">\n<size>0</size>\n<r-size>0</r-size>\n<name></name>\n<desc></desc>\n<requirements-"+new_entry_id+">\n</requirements-"+new_entry_id+">\n</"+new_entry_id+">\n"+file_text[new_entry_pos:]
        elif parent_entry_size==0:
            new_entry_pos=file_text.find("</"+parent_entry_id+">")
            file_text_new=file_text[:new_entry_pos]+"<"+insert_type+">\n<"+new_entry_id+">\n<size>0</size>\n<r-size>0</r-size>\n<name></name>\n<desc></desc>\n<requirements-"+new_entry_id+">\n</requirements-"+new_entry_id+">\n</"+new_entry_id+">\n</"+insert_type+">\n"+file_text[new_entry_pos:]

    file_text_new=file_text_new.replace("<"+parent_entry_id+">\n<size>"+str(parent_entry_size)+"</size>","<"+parent_entry_id+">\n<size>"+new_entry_number+"</size>")

    replace_project_tree(project, file_text_new)
    # parent.number_of_children_entries=new_entry_number

    return new_entry_id


def replace_project_tree(project, new_tree_text):
    project.project_tree = new_tree_text
    project.save()
