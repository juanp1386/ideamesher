from .models import Entry
from django.shortcuts import get_object_or_404
import io

class TreeSVG():

    def __init__(self):
        self.x_position=0
        self.y_position=0
        self.x_true_position=0
        self.y_true_position=0
        self.tree_SVG=""

        self.entry_size=0
        self.requirements_size=0
        self.name_text=""
        self.desc_text=""
        self.entry_type=""
        self.entry_text=""
        self.project=""
        self.lines=None

    def draw_branches(self, current_line_number):
        print("project2: "+self.project+"-")
        decendant_horizontal_line_x_start=self.x_position
        decendant_horizontal_line_y_start=self.y_position

        draw_line=False
        loop=True

        draw_line=False
        loop=True

        while loop:
            if len(self.lines) > current_line_number :
                line=self.lines[current_line_number]
                line_text=line.replace('\n', '').strip()
                # print("line-text: "+line_text)

                if "<size>" in line_text:
                    self.entry_size=line_text.replace('<size>','').replace('</size>','')
                elif "<r-size>" in line_text:
                    self.requirements_size=line_text.replace('<r-size>','').replace('</r-size>','')
                elif line_text=="<concepts>" or line_text=="<designs>" or line_text=="<validations>":
                    self.x_position=self.x_position+1
                    self.y_position=self.y_position-1
                    if line_text=="<concepts>":
                        self.entry_type="concept"
                    elif line_text=="<designs>":
                        self.entry_type="design"
                    else:
                        self.entry_type="validation"

                elif line_text=="</concepts>" or line_text=="</designs>" or line_text=="</validations>":
                    self.x_position=self.x_position-1
                    if line_text=="</concepts>":
                        self.entry_type="requirement"
                    elif line_text=="</designs>":
                        self.entry_type="requirement"
                        #self.draw_line(71+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 71+decendant_horizontal_line_x_start*72, self.y_position*46-25, self.entry_text, self.entry_type)
                    else:
                        self.entry_type="design"
                    # self.draw_line(71+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 71+decendant_horizontal_line_x_start*72, self.y_position*46-25, self.entry_text, self.entry_type)
                elif "</requirements-" in line_text:
                    self.entry_type="concept"
                elif "<requirements-" in line_text:
                    self.entry_type="requirement"

                elif '<' +self.project in line_text:

                    self.entry_text=line_text.replace('<','').replace('>','')
                    print("entry text: "+line_text.replace('<','').replace('>',''))
                    self.y_position=self.y_position+1
                    if self.entry_type == "requirement":
                        self.draw_rectangle(7+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-40, 65+decendant_horizontal_line_x_start*72, self.y_position*46-5) # for requirements
                    else:
                        self.draw_line(71+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 71+decendant_horizontal_line_x_start*72, self.y_position*46-25, self.entry_text, self.entry_type)

                    current_line_number=self.draw_branches(current_line_number+1)

                elif "</"+self.project in line_text:

                    if self.entry_type=="requirement":
                        pass
                    else:
                        self.draw_line(decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 15+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, self.entry_text, self.entry_type)
                    if self.entry_type=="validation":
                        pass
                    else:
                        self.draw_line(50+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 75+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, self.entry_text, self.entry_type)


                    if self.entry_type=="concept":
                        pass
                    else:
                        # if int(self.entry_size)>0:
                        #     self.draw_line(71+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 71+decendant_horizontal_line_x_start*72, self.y_position*46-25)
                        # self.draw_line(71+decendant_horizontal_line_x_start*72, decendant_horizontal_line_y_start*46-25, 71+decendant_horizontal_line_x_start*72, self.y_position*46-25, self.entry_text, self.entry_type)
                        pass

                    return current_line_number
                elif "<name>" in line_text:
                    self.name_text=line_text.replace('<name>','').replace('</name>','')
                elif "<desc>" in line_text:
                    self.desc_text=line_text.replace('<desc>','').replace('</desc>','')
                    entry_to_show=self.entry_text;
                    name_to_show=self.name_text;
                    desc_to_show=self.desc_text;
                    self.draw_button(self.entry_text.rsplit('\\', 1)[-1], entry_to_show, self.x_position*72+5, self.y_position*46-32)

                    # entry=Button(scroll_frame, text=self.entry_type.rsplit('\\', 1)[-1], relief='flat', width="6",height="1",command=lambda the_entry_to_show=entry_to_show, the_name_to_show=name_to_show, the_desc_to_show=desc_to_show, the_entry_type=self.entry_type, the_entry_size=self.entry_size, the_requirements_size=self.requirements_size :input_data(the_entry_to_show,the_name_to_show, the_desc_to_show, the_entry_type, the_entry_size, the_requirements_size))
                    # entry.grid(column=self.x_position,row=self.y_position)
            else:
                loop=False
            current_line_number=current_line_number+1



    def draw_tree(self, project_tree):
        f=io.StringIO(project_tree)
        self.entry_type="requirement"
        self.lines=f.readlines()
        first_line=self.lines[0]
        self.project=first_line.replace('\n', '').strip()
        self.project=self.project.replace('<','')
        self.project=self.project.replace('>','')
        print("project: "+self.project)
        self.draw_branches(0)

        return self.tree_SVG

    def draw_line(self, x_start, y_start, x_end, y_end, id, type): #adds an SVG line element to the tree_SVG
        self.tree_SVG=self.tree_SVG+\
            '<line class= "tree_line '+id+' '+type+'"" x1="'+str(x_start)+'" y1="'+str(y_start)+'" x2="'+str(x_end)+'" y2="'+str(y_end)+'"/>'
    def draw_rectangle(self, x_start, y_start, x_end, y_end): #adds an SVG rectangle element to the tree_SVG
        self.tree_SVG=self.tree_SVG+\
            '<rect class= "req_rectangle" x="'+str(x_start)+'" y="'+str(y_start)+'" ry="5" width="'+str(x_end-x_start)+'" height="'+str(y_end-y_start)+'"/>'
    def draw_button(self, text_to_display, this_entry_id,  x_start, y_start):
        entry=Entry.objects.get(entry_id=this_entry_id)
        entry_pk=entry.pk
        publish_status="not_published"
        if entry.published_date:
            publish_status="published"

        self.tree_SVG=self.tree_SVG+\
            '<a class="tree_link" id="'+str(entry_pk)+'" target="_self" cursor="pointer">\
                <g class="tree_button_group">\
                  <rect class="tree_button" x="'+str(x_start)+'" y="'+str(y_start)+'" ry="4"  width="60" height="15"/>\
                  <text class="tree_button_text '+  publish_status + '" x="'+str(x_start+22)+'" y="'+str(y_start+12)+'">'+text_to_display+'</text>\
                </g>\
            </a>'
