
(* 2019 (C) Aalto University, Jussi Rintanen *)

(******* Implementation of normal forms in Standard ML *******)

datatype 'a formula = AND of 'a formula list
		    | OR of 'a formula list
		    | NOT of 'a formula
		    | TRUE
		    | FALSE
		    | ATOM of 'a;

(*
  Literals    : Pos x and Neg x for atoms x
  Clauses     : list of literals
  Clause sets : list of clauses
  Here type of atoms left open, so we could use integers, strings, or
  something else.
*)

datatype 'a lit = Pos of 'a
		| Neg of 'a;

fun product (a,b) = foldl (fn (a,s) => foldl (fn (b,s) => (a,b)::s) s b) [] a;
fun compl (Neg a) = Pos a
  | compl (Pos a) = Neg a;

(***** Module specification *****)

signature NFSIG =
  sig
    val mkDNF : 'a formula -> 'a lit list list
    val mkCNF : 'a formula -> 'a lit list list
    val mkNNF : 'a formula -> 'a formula
  end;

(***** Module implementation *****)

structure NF : NFSIG =
  struct

    (* For clause sets [c1,c2,...,cn], [d1,d2,...,dm], ...
      compute a clause set that is equivalent to the disjunction
      of these sets. This is obtained by forming the Cartesian product
      of these sets as
         [(c1,d1,...), (c1,d2,...),...,(c2,c1,...),(c2,d2,...),...]
      and then merging each of these tuples together to clauses as
         [c1@d1@...,c1@d2@...,...,c2@d1@...,c2@d2@...,...]
    *)

    fun clauseproduct ([],ac) = [[]]@ac
      | clauseproduct ([cs],ac) = cs@ac
      | clauseproduct (cs::css,ac) =
	let val css0 = clauseproduct (css,[])
	in
	    (map (op @) (product(cs,css0)))@ac
	end

    (* Negate the formula, but move the negation deeper in front of atoms *)

    fun negin (AND fs) = OR(map negin fs)
      | negin (OR fs) = AND(map negin fs)
      | negin (NOT f) = f
      | negin TRUE = FALSE
      | negin FALSE = TRUE
      | negin (ATOM a) = NOT(ATOM a)

    (* Recursively produce a clause set equivalent to the formula *)
		      
    fun mkClauses(AND fs,ac) = foldr mkClauses ac fs
      | mkClauses(OR fs,ac) = clauseproduct(map (fn f => mkClauses(f,[])) fs,ac)
      | mkClauses(TRUE,ac) = ac
      | mkClauses(FALSE,ac) = []::ac
      | mkClauses(NOT(ATOM v),ac) = [Neg v]::ac
      | mkClauses(ATOM v,ac) = [Pos v]::ac
      | mkClauses(NOT f,ac) = mkClauses(negin f,ac)

    fun mkCNF e = mkClauses(e,[])
    fun mkDNF e = map (map compl) (mkClauses(NOT e,[]))

    fun mkNNF(NOT f) = negin (mkNNF f)
      | mkNNF(AND fs) = AND(map mkNNF fs)
      | mkNNF(OR fs) = OR(map mkNNF fs)
      | mkNNF f = f

  end;
