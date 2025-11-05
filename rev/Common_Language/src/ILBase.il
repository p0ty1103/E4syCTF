.assembly extern mscorlib {}
.assembly ILBase {}
.module ILBase.exe

.class public auto ansi beforefieldinit ILBase
       extends [mscorlib]System.Object
{
  .method public hidebysig specialname rtspecialname 
          instance void .ctor() cil managed
  {
    ldarg.0
    call instance void [mscorlib]System.Object::.ctor()
    ret
  }

  .method public hidebysig static int32  Main(string[] args) cil managed
  {
    .entrypoint
    .maxstack  6
    .locals init (
      [0] string inp,
      [1] uint8[] inpb,
      [2] uint8[] flagb,
      [3] int32 i)

    // print prompt
    ldstr      "INPUT FLAG > "
    call       void [mscorlib]System.Console::Write(string)

    // read input
    call       string [mscorlib]System.Console::ReadLine()
    stloc.0

    // if inp.Length <> 41 then print "NO." and return -1
    ldloc.0
    callvirt   instance int32 [mscorlib]System.String::get_Length()
    ldc.i4.s   41
    ceq
    brtrue.s   LENGTH_OK

    ldstr      "NO."
    call       void [mscorlib]System.Console::WriteLine(string)
    ldc.i4.m1
    ret

  LENGTH_OK:
    // Convert input and expected flag to ASCII bytes
    call       class [mscorlib]System.Text.Encoding [mscorlib]System.Text.Encoding::get_ASCII()
    ldloc.0
    callvirt   instance unsigned int8[] [mscorlib]System.Text.Encoding::GetBytes(string)
    stloc.1

    call       class [mscorlib]System.Text.Encoding [mscorlib]System.Text.Encoding::get_ASCII()
    ldstr      "E4syCTF{d0tn3t_h4s_4_CLR_50_634utifu1...}"
    callvirt   instance unsigned int8[] [mscorlib]System.Text.Encoding::GetBytes(string)
    stloc.2

    // i = 0
    ldc.i4.0
    stloc.3

  LOOP_START:
    // if i >= 41 -> success
    ldloc.3
    ldc.i4.s   41
    bge.s      EQUAL_OK

    // compare inpb[i] and flagb[i]
    ldloc.1
    ldloc.3
    ldelem.u1
    ldloc.2
    ldloc.3
    ldelem.u1
    ceq
    brtrue.s   NEXT_CHAR

    // mismatch -> NO., return -1
    ldstr      "NO."
    call       void [mscorlib]System.Console::WriteLine(string)
    ldc.i4.m1
    ret

  NEXT_CHAR:
    // i++
    ldloc.3
    ldc.i4.1
    add
    stloc.3
    br.s       LOOP_START

  EQUAL_OK:
    ldstr      "COLLECT:)"
    call       void [mscorlib]System.Console::WriteLine(string)
    ldc.i4.1
    ret
  }
}


