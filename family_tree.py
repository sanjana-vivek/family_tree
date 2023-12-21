from collections import defaultdict
from collections import deque
from queue import Queue
import graphviz
from graphviz import nohtml

class Graph:
    def __init__(self):
        self.graph = defaultdict()

    def add_vertex(self, vertex):
        if vertex in self.graph:
            print(vertex, "already exists")
        else:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.graph.keys():
            print(vertex1, "does not exist")
        elif vertex2 not in self.graph.keys():
            print(vertex2, "does not exist")
        else:
            self.graph[vertex1].append((vertex2, weight))

    def vertices(self):
        return self.graph.keys()

    def edges(self, vertex):
        # print(self.graph[vertex])
        return self.graph[vertex]

    def edit_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.graph.keys():
            print(vertex1, "does not exist")
        elif vertex2 not in self.graph.keys():
            print(vertex2, "does not exist")
        else:
            for i in range(len(self.graph[vertex1])):
                if self.graph[vertex1][i][0] == vertex2:
                    self.graph[vertex1][i] = (vertex2, weight)
                    break

    def edit_vertex(self, old_vertex, new_vertex):
        if old_vertex not in self.graph.keys():
            print(old_vertex, "does not exist")
        elif new_vertex in self.graph.keys():
            print(new_vertex, "already exists")
        else:
            # Update the existing vertex with the new one
            self.graph[new_vertex] = self.graph.pop(old_vertex)

    def delete_vertex(self, vertex):
        if vertex not in self.graph.keys():
            print(vertex, "does not exist")
        else:
            self.graph.pop(vertex)
            for key in self.graph.keys():
                for tupl in self.graph[key]:
                    if tupl[0] == vertex:
                        self.graph[key].remove((tupl))
                        break

    # def __init__(self):
    # return iter(self.graph.values())
    def is_empty(self):
        return bool(self.graph)

    def print_graph(self):  # For checking purposes in the code for the coder
        for vertex in self.graph:
            for edges in self.graph[vertex]:
                print(vertex, "->", edges[0], "edge weight:", edges[1])



class Person:
    def __init__(self, name, gender, mid, age=0):  # ,adopted=None):
        self.name = name
        self.gender = gender
        self.age = age
        # self.adopted=adopted
        self.mid = mid

    def edit_person_name(self, name):
        self.name = name

    def edit_person_gender(self, gender):
        self.gender = gender

    def edit_person_age(self, age):
        self.age = age

    # def edit_person_adopted(self,adopted):
    #   self.adopted=adopted
    def key(self):
        return (self.name, self.gender, self.age)  # self.adopted,

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.key() == other.key()
        return False

    def __str__(self):
        return self.name + "(" + self.gender + ")"

    def dot(self):
        return nohtml(f'{self.gender}|<f1> {self.name}|{self.age}')

class FamilyTree:
    def __init__(self):
        self.family = Graph()
        self.tree_members = []
        self.tree_ids = []
        self.dot = graphviz.Digraph(
            "Family-Tree",
            comment="Family Tree comment",
            format="png",
            node_attr={"shape": "record", "height": ".1"},
        )

    def add_family_member(self, person):
        assert person not in self.family.vertices(), "The person already exists"
        self.family.add_vertex(person)
        self.tree_members.append(person)
        self.tree_ids.append(person.mid)
        self.dot.node(f"NODE-{hash(person)}", person.dot())

    def add_relationship(self, person1, person2, relationship):
        assert person1 != person2, "person1=person2"
        weight = self.relationship_to_weight(relationship)
        self.family.add_edge(person1, person2, weight)
        self.family.add_edge(person2, person1, self.counter_weight(weight))
        self.dot.edge(f"NODE-{hash(person1)}:f1",
                          f"NODE-{hash(person2)}:f1",
                          label=relationship)

    def counter_weight(self, weight):
        return {
            10: 10,
            11: 11,
            12: 12,
            13: 14,
            14: 13,
        }[weight]

    def relationship_to_weight(self, relationship):
        return {
            "Divorced": 10,
            "Married": 11,
            "Sibling": 12,
            "Parent": 13,
            "Son-Daughter": 14,
        }[relationship]

    def editMemberName(self, pid, new_name):
        old_member = self.tree_members[pid]
        new_member = Person(
            new_name, old_member.gender, old_member.mid, old_member.age
        )  # old_member.adopted,old_member.age)
        self.family.edit_vertex(old_member, new_member)
        self.tree_members[pid].edit_person_name(new_name)

    def editMemberGender(self, pid, new_gender):
        old_member = self.tree_members[pid]
        new_member = Person(
            old_member.name, new_gender, old_member.mid, old_member.age
        )  # old_member.adopted,
        self.family.edit_vertex(old_member, new_member)
        self.tree_members[pid].edit_person_gender(new_gender)

    def editMemberAge(self, pid, new_age=0):
        old_member = self.tree_members[pid]
        new_member = Person(
            old_member.name, old_member.gender, old_member.mid, new_age
        )  # old_member.adopted,
        self.family.edit_vertex(old_member, new_member)
        self.tree_members[pid].edit_person_age(new_age)

    # def editMemberAdoption(self,pid,new_adopted=None):
    # old_member=self.tree_members[pid]
    # new_member=Person(old_member.name,old_member.gender,new_adopted,old_member.age)
    # self.family.edit_vertex(old_member,new_member)
    # self.tree_members[pid].edit_person_adopted(new_adopted)
    def edit_relationship(self, person1, person2, relationship):
        weight = self.relationship_to_weight(relationship)
        self.family.edit_edge(person1, person2, weight)
        self.family.edit_edge(person2, person1, self.counter_weight(weight))
        self.dot.edge(f"NODE-{hash(person1)}:f1",
                          f"NODE-{hash(person2)}:f1",
                          label=relationship)

    def delete_family_member(self, person):
        assert (
            person in self.family.vertices()
        ), "this person does not exist in the family tree"
        self.family.delete_vertex(person)
        self.tree_ids.remove(person.mid)
        self.tree_members.remove(person)

    def member_relatives(self, person):
        return self.family.edges(person)

    def find_relatives_bfs(self, person):
        visited = set()
        relatives = set()
        queue = deque([person])

        while queue:
            current_person = queue.popleft()
            if current_person not in visited:
                relatives.add(current_person)
                visited.add(current_person)

                for relative, _ in self.family.edges(current_person):
                    if relative not in visited:
                        queue.append(relative)

        relatives.remove(person)  # Remove the starting person
        return relatives

    def delete_all(self):
        for i in range(len(self.tree_members)):
            self.family.delete_vertex(self.tree_members[i])
        self.tree_members.clear()

    def print_dot(self):
        print(self.dot)

    def weight_to_relationship(self, weight):
        return {
            10: "Divorced",
            11: "Married",
            12: "Sibling",
            13: "Parent",
            14: "Son-Daughter",
        }[weight]

    def print_family_tree(self):
        for i in range(len(self.tree_members)):
            person = self.tree_members[i]
            edges = self.member_relatives(person)
            print(person, "{id:" + str(i + 1) + "}")
            for relative, weight in edges:
                print(" ", self.weight_to_relationship(weight), "\t", str(relative))
        print("DOT file...")
        self.print_dot()

    def view(self):
        self.dot.view()

d = 0
ft = FamilyTree()
while d == 0:
    option = input(
        "1.Initialize Family Tree\n2.Add new member\n3.Add relationship with existing members\n4.Visualize Family member information\n5.Edit family member\n6.Edit Family member relationship\n7.Delete Family member\n8.Find relatives of a family member\n9.Visualize Family Tree\n10.Exit\n"
    )
    if option == "1":
        a = 1
        print("First Person")
        na = input("Name : ")
        ge = input("Gender : ")
        ag = input("Age : ")
        child = Person(na, ge, 1, ag)
        # child.age=23
        ft.add_family_member(child)
        c = 0
        while c == 0:
            choice = input("First Person's Relations : Parent/Partner/Sibling/None : \n")
            if choice == "Parent":
                n = input("Father Name\n")
                # g=input("Father Gender\n")
                g = "M"
                h = input("Father age\n")
                a = a + 1
                dad = Person(n, g, a, h)
                # dad.age=h
                n1 = input("Mother Name\n")
                # g1=input("Mother Gender\n")
                g1 = "F"
                h1 = input("Mother age\n")
                a = a + 1
                mom = Person(n1, g1, a, h1)
                # mom.age=h1
                ft.add_family_member(dad)
                ft.add_family_member(mom)
                ft.add_relationship(dad, mom, "Married")
                # ft.add_relationship(dad,child,"Son-Daughter")
                ft.add_relationship(child, dad, "Parent")
                # ft.add_relationship(mom,child,"Son-Daughter")
                ft.add_relationship(child, mom, "Parent")
                if ft.family.edges(child):
                    siblings = [
                        s
                        for s, w in ft.family.edges(child)
                        if ft.weight_to_relationship(w) == "Sibling"
                    ]
                    for sibling in siblings:
                        # Create Son-Daughter relationship between the new member and the siblings of the existing sibling
                        if sibling != dad or sibling != mom:
                            ft.add_relationship(mom, sibling, "Son-Daughter")
                            ft.add_relationship(sibling, dad, "Parent")
            elif choice == "Sibling":
                n = input("Sibling Name\n")
                g = input("Sibling Gender\n")
                aa = input("Sibling Age\n")
                a = a + 1
                sib = Person(n, g, a, aa)
                ft.add_family_member(sib)
                ft.add_relationship(sib, child, "Sibling")

                # Check if the first person (child) has parents and create relationships
                if ft.family.edges(child):
                    siblings = [
                        s
                        for s, w in ft.family.edges(child)
                        if ft.weight_to_relationship(w) == "Sibling"
                    ]
                    for sibling in siblings:
                        if sibling != sib:
                            ft.add_relationship(sib, sibling, "Sibling")

                    parents = [
                        parent
                        for parent, w in ft.family.edges(child)
                        if ft.weight_to_relationship(w) == "Parent"
                    ]
                    for parent in parents:
                        ft.add_relationship(sib, parent, "Parent")
            elif choice == "Partner":
                n = input("Partner Name\n")
                g = input("Partner Gender\n")
                aa = input("Partner Age\n")
                a = a + 1
                par = Person(n, g, a, aa)
                # par.age=20
                ft.add_family_member(par)
                ft.add_relationship(child, par, "Married")
            elif choice == "None":
                c = c + 1
            else:
                print("Please enter Valid Input")
    elif option == "2":
        per = input("Name:\n")
        perg = input("Gender:\n")
        pera = int(input("Age:\n"))
        a = a + 1
        p = Person(per, perg, a, pera)
        ft.add_family_member(p)
        pid2 = int(input("Enter the related family member id: "))
        rel = input("Related member is (Divorced/Married/Son-Daughter/Parent/Sibling) of new member?:")
        p1 = ft.tree_members[a - 1]
        p2 = ft.tree_members[pid2 - 1]
        ft.add_relationship(p1, p2, rel)
        if rel == "Son-Daughter" and ft.family.edges(p2):
            siblings = [
                s
                for s, w in ft.family.edges(p2)
                if ft.weight_to_relationship(w) == "Sibling"
            ]
            for sibling in siblings:
                # Create Son-Daughter relationship between the new member and the siblings of the existing sibling
                if sibling != p1:
                    ft.add_relationship(p1, sibling, "Son-Daughter")
                    # ft.add_relationship(sibling, p1, "Parent")
        if rel == "Sibling":
            if ft.family.edges(p2):
                siblings = [
                    s
                    for s, w in ft.family.edges(p2)
                    if ft.weight_to_relationship(w) == "Sibling"
                ]
                for sibling in siblings:
                    if sibling != p1:
                        ft.add_relationship(p1, sibling, "Sibling")

                parents = [
                    parent
                    for parent, w in ft.family.edges(p2)
                    if ft.weight_to_relationship(w) == "Parent"
                ]
                for parent in parents:
                    ft.add_relationship(p1, parent, "Parent")
    elif option == "3":
        pid1 = int(input("Enter member id: "))
        pid2 = int(input("Enter member id: "))
        rel = input("Divorced/Married/Son-Daughter/Parent/Sibling :")
        p1 = ft.tree_members[pid1 - 1]
        p2 = ft.tree_members[pid2 - 1]
        ft.add_relationship(p1, p2, rel)
    elif option == "4":
        p1 = int(input("Member id "))
        pp = ft.tree_members[p1 - 1]
        print("Name:" + pp.name)
        print("Gender: " + pp.gender)
        print("Age: " + str(pp.age))
        # print("Adopted: "+str(pp.adopted))
    elif option == "5":
        pid = int(input("Edit member: "))
        pid = pid - 1
        ch = input("Name/Age/Gender: ")
        if ch == "Name":
            n = input("Name: ")
            ft.editMemberName(pid, n)
        if ch == "Age":
            a = int(input("Age: "))
            ft.editMemberAge(pid, a)
        if ch == "Gender":
            g = input("Gender: ")
            ft.editMemberGender(pid, g)
    elif option == "6":
        pid1 = int(input("enter member1 id: "))
        pid2 = int(input("enter member2 id: "))
        rel = input("Divorced/Married ")
        for i in range(0, len(ft.tree_ids)):
            if pid1 == ft.tree_ids[i]:
                p1 = ft.tree_members[i]
        for i in range(0, len(ft.tree_ids)):
            if pid2 == ft.tree_ids[i]:
                p2 = ft.tree_members[i]
        ft.edit_relationship(p1, p2, rel)
    elif option == "7":
        pid = int(input("Enter member id"))
        p = ft.tree_members[pid - 1]
        ft.delete_family_member(p)
    elif option == "8":
        pi = int(input("Enter member id :"))
        person_to_find_relatives = ft.tree_members[
            pi - 1
        ]  # Choose a person to find relatives for
        relatives = ft.find_relatives_bfs(person_to_find_relatives)
        print(f"All relatives of {person_to_find_relatives}:")
        for relative in relatives:
            print(relative)
    elif option == "9":
        # visualization
        ft.view()

    elif option == "10":
        break

    ft.print_family_tree()
